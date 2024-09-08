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

import dataclasses
import typing
import uuid

import sqlalchemy.ext.asyncio
from sqlalchemy import UUID, String, select
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
        UUID(as_uuid=True).with_variant(String(32), "sqlite"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64))


T_DDDEntityModel = typing.TypeVar('T_DDDEntityModel', bound=DDDModel)


class DDDEntity(typing.Generic[T_DDDEntityModel]):
    """
    Base class for all domain entities. It requires a generic entity model as its persisted peer.
    """
    model: typing.Type[T_DDDEntityModel]

    def __init__(self, name: str, *args, **kwargs) -> None:
        if self.model is None:
            raise DDDException(code=500, msg='Misconfigured DDDEntity without model')
        self._uid: UniqueIdentifier = uuid.uuid4()
        self._name = name
        self._dirty = True

    async def post_create(self) -> None:
        """
        This async hook function is called after the entity is first persisted
        Raises:
            EntityInvariantException
        """
        pass

    async def post_modify(self) -> None:
        """
        This async hook function is called after changes to the entity have been persisted
        Raises:
            EntityInvariantException
        """
        pass

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

    @classmethod
    async def from_model(cls, model: T_DDDEntityModel, *args, **kwargs) -> typing.Self:
        entity = cls(model.name, *args, **kwargs)
        entity._uid = UniqueIdentifier(model.uid)
        return entity

    async def to_model(self) -> T_DDDEntityModel:
        model = self.model()
        model.uid = str(self._uid)
        model.name = self._name
        return model

    def __hash__(self) -> int:
        return hash(self._uid)

    def __eq__(self, other: typing.Any) -> bool:
        return any([
            self.__class__ == other.__class__,
            self._uid == other.uid,
            self._name == other.name
        ])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(uid={self._uid}, name={self._name})'


T_DDDEntity = typing.TypeVar("T_DDDEntity", bound=DDDEntity)


class DDDAggregateRoot(DDDEntity[T_DDDEntityModel]):
    """
    An aggregate root class.

    Only aggregate roots have corresponding repositories
    """
    repository: typing.ClassVar['DDDRepository']

    async def save(self) -> None:
        if not self._dirty:
            return
        await self.repository.create(self)
        self._dirty = False

    async def remove(self) -> None:
        await self.repository.remove(self)


T_DDDAggregateRoot = typing.TypeVar("T_DDDAggregateRoot", bound=DDDAggregateRoot)


class DDDRepository(typing.Generic[T_DDDAggregateRoot]):
    """
    Base class for all repositories

    Limitations:
    * typing.ClassVar does not yet support type variables so we might constrain it on the superclass
      but that then further confuses the type checker
    """
    entity_class: typing.Type[T_DDDAggregateRoot]

    def __init__(self, session_maker: sqlalchemy.ext.asyncio.async_sessionmaker) -> None:
        if self.entity_class is None:
            raise DDDException(code=500, msg='Misconfigured DDDRepository without entity')
        self._session_maker = session_maker
        self._identity_map: typing.Dict[UniqueIdentifier, T_DDDAggregateRoot] = {}
        self.entity_class.repository = self

    async def get_by_uid(self, uid: UniqueIdentifier) -> T_DDDAggregateRoot:
        if uid in self._identity_map:
            return self._identity_map[uid]
        async with self._session_maker() as session:
            model = await session.get(self.entity_class.model, str(uid))
            if model is None:
                raise EntityNotFoundException()
            self._identity_map[uid] = await self.entity_class.from_model(model)
            return self._identity_map[uid]

    async def list(self) -> typing.List[T_DDDAggregateRoot]:
        async with self._session_maker() as session:
            models = (await session.scalars(select(self.entity_class.model))).all()
            return [await self.entity_class.from_model(m) for m in models]

    async def create(self, entity: T_DDDAggregateRoot) -> T_DDDAggregateRoot:
        if entity.uid in self._identity_map:
            return await self.modify(entity)
        async with self._session_maker() as session:
            async with session.begin():
                model = await entity.to_model()
                session.add(model)
            entity._uid = model.uid
            self._identity_map[entity.uid] = entity
        await entity.post_create()
        return self._identity_map[entity.uid]

    async def modify(self, entity: T_DDDAggregateRoot) -> T_DDDAggregateRoot:
        async with self._session_maker() as session:
            session.add(await entity.to_model())
        await entity.post_modify()
        return entity

    async def remove(self, entity: T_DDDAggregateRoot) -> None:
        await entity.pre_remove()
        async with self._session_maker() as session:
            model = await session.get(self.entity_class.model, str(entity.uid))
            if model is None:
                raise EntityNotFoundException()
            await session.delete(model)
