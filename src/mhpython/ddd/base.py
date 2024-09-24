#  MIT License
#
#  Copyright (c) 2024 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
import dataclasses
import typing
import uuid

import sqlalchemy.ext.asyncio
from sqlalchemy import UUID, String, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#
# A type var for a unique identifier

UniqueIdentifier = uuid.UUID


class DDDException(Exception):
    """
    A base exception
    """

    def __init__(self, code: int, msg: str) -> None:
        super().__init__()
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    def __str__(self) -> str:
        return f'[{self._code}] {self._msg}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(code={self._code}, msg={self._msg})'


class EntityNotFoundException(DDDException):
    """
    Exception thrown when no entity can be found
    """

    def __init__(self, code: int = 404, msg: str = 'The specified entity does not exist') -> None:
        super().__init__(code, msg)


class EntityInvariantException(DDDException):
    """
    Exception thrown when there is something wrong with the entity
    """
    pass


#
# Core DDD classes


@dataclasses.dataclass(frozen=True)
class DDDValueObject:
    """
    Base class for all value objects. The T_DDDValueObject type var binds Generics to subclasses.
    """
    pass


T_DDDValueObject = typing.TypeVar('T_DDDValueObject', bound=DDDValueObject)


class DDDModel(DeclarativeBase):
    """
    Base class for all persistent entities. The T_DDDEntityModel type var binds Generics to
    subclasses.
    """
    __abstract__ = True
    uid: Mapped[str] = mapped_column(
        UUID(as_uuid=True).with_variant(String(32), "sqlite"),
        primary_key=True,
        sort_order=-1       # Make sure uid is the first column
    )
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f'{self.__class__.__name__}(uid={self.uid}, name={self.name})'


T_DDDModel = typing.TypeVar('T_DDDModel', bound=DDDModel)


class DDDEntity(typing.Generic[T_DDDModel]):
    """
    Base class for all domain entities. It requires a generic entity model as its persisted peer.
    """
    repository: typing.ClassVar['DDDRepository']

    def __init__(self, name: str, *args, **kwargs) -> None:
        self._uid: UniqueIdentifier = uuid.uuid4()
        self._name = name
        self._dirty = True

    async def post_create(self) -> None:
        """
        This async hook function is called after the entity is first persisted
        Raises:
            EntityInvariantException
        """
        self._dirty = False

    async def post_modify(self) -> None:
        """
        This async hook function is called after changes to the entity have been persisted
        Raises:
            EntityInvariantException
        """
        self._dirty = False

    async def pre_remove(self) -> None:
        """
        This async hook function is called before the entity is removed from persistence
        Raises:
            EntityInvariantException
        """
        pass

    @property
    def dirty(self) -> bool:
        return self._dirty

    @dirty.setter
    def dirty(self, value: bool) -> None:
        self._dirty = value

    @property
    def uid(self) -> UniqueIdentifier:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self._dirty = True

    def __hash__(self) -> int:
        return hash(self._uid)

    def __eq__(self, other: typing.Any) -> bool:
        return all([
            other is not None,
            self.__class__ == other.__class__,
            self._uid == other.uid,
            self._name == other.name
        ])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(uid={self._uid}, name={self._name})'


T_DDDEntity = typing.TypeVar("T_DDDEntity", bound=DDDEntity)


class DDDAggregateRoot(DDDEntity[T_DDDModel]):
    """
    An aggregate root class.
    Only aggregate roots have save and remove functions.
    """
    async def save(self) -> typing.Self:
        if not self._dirty:
            return self
        await self.repository.create(self)
        return self

    async def remove(self) -> None:
        await self.repository.remove(self)


T_DDDAggregateRoot = typing.TypeVar("T_DDDAggregateRoot", bound=DDDAggregateRoot)


class DDDRepository(typing.Generic[T_DDDEntity, T_DDDModel], abc.ABC):
    """
    Base class for all repositories

    Limitations:
    * typing.ClassVar does not yet support type variables so we might constrain it on the superclass
      but that then further confuses the type checker
    """
    entity_class: typing.Type[T_DDDEntity]
    model_class: typing.Type[T_DDDModel]

    def __init__(self, session_maker: sqlalchemy.ext.asyncio.async_sessionmaker) -> None:
        if self.entity_class is None:
            raise DDDException(code=500, msg='Misconfigured DDDRepository without entity')
        if self.model_class is None:
            raise DDDException(code=500, msg='Misconfigured DDDRepository without model')
        self._session_maker = session_maker
        self._identity_map: typing.Dict[UniqueIdentifier, T_DDDEntity] = {}
        self.entity_class.repository = self

    async def get_by_uid(self, uid: UniqueIdentifier) -> T_DDDEntity:
        try:
            if uid in self._identity_map:
                return self._identity_map[uid]
            async with self._session_maker() as session:
                model = await session.get(self.model_class, str(uid))
                if model is None:
                    raise EntityNotFoundException()
                self._identity_map[uid] = await self.from_model(model)
                return self._identity_map[uid]
        except SQLAlchemyError as sae:
            raise DDDException(code=500, msg='Failure getting the entities') from sae

    async def list(self) -> typing.List[T_DDDEntity]:
        try:
            async with self._session_maker() as session:
                models = (await session.scalars(select(self.model_class))).all()
                return [await self.from_model(m) for m in models]
        except SQLAlchemyError as sae:
            raise DDDException(code=500, msg='Failure listing entities from persistence') from sae

    async def create(self, entity: T_DDDEntity) -> T_DDDEntity:
        try:
            if not issubclass(type(entity), DDDAggregateRoot):
                raise EntityInvariantException(code=400, msg='Only aggregate roots can be created')
            if entity.uid in self._identity_map:
                return await self.modify(entity)
            async with self._session_maker() as session, session.begin():
                model = await self.to_model(entity)
                session.add(model)
                entity._uid = UniqueIdentifier(model.uid)
                self._identity_map[entity.uid] = entity
                await entity.post_create()
            return self._identity_map[entity.uid]
        except SQLAlchemyError as sae:
            raise DDDException(code=500, msg='Failure persisting the entities') from sae

    async def modify(self, entity: T_DDDEntity) -> T_DDDEntity:
        try:
            if not entity.uid in self._identity_map:
                raise EntityInvariantException(code=400, msg='This entity is unknown to the repository')
            async with self._session_maker() as session, session.begin():
                persisted = await session.get(self.model_class, str(entity.uid))
                model = await self.to_model(entity, persisted)
                session.add(model)
                await entity.post_modify()
            return entity
        except SQLAlchemyError as sae:
            raise DDDException(code=500, msg='Failure persisting the entities') from sae

    async def remove(self, entity: T_DDDEntity) -> None:
        try:
            await entity.pre_remove()
            async with self._session_maker() as session, session.begin():
                model = await session.get(self.model_class, str(entity.uid))
                if model is None:
                    raise EntityNotFoundException()
                await session.delete(model)
        except SQLAlchemyError as sae:
            raise DDDException(code=500, msg='Failure removing the entities in persistent store') from sae

    @classmethod
    @abc.abstractmethod
    async def from_model(cls, model: T_DDDModel, *args, **kwargs) -> T_DDDEntity:
        entity = cls.entity_class(name=model.name, *args, **kwargs)
        entity._uid = UniqueIdentifier(model.uid)
        return entity

    @classmethod
    @abc.abstractmethod
    async def to_model(cls, entity: T_DDDEntity, persisted: T_DDDModel | None = None) -> T_DDDModel:
        if persisted is None:
            model = cls.model_class()
            model.uid = str(entity.uid)
        else:
            model = persisted
        model.name = entity.name
        return model

    def __repr__(self):
        return f'{self.__class__.__name__}({self.entity_class})'
