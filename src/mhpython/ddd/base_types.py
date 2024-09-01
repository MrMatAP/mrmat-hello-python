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

    def __init__(self, code: int = 400, msg: str = 'The specified entity does not exist') -> None:
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


class DDDEntityModel(DeclarativeBase):
    """
    Base class for all persistent entities. The T_DDDEntityModel type var binds Generics to
    subclasses.
    """
    __abstract__ = True
    uid: Mapped[str] = mapped_column(
        UUID(as_uuid=True).with_variant(String(32), "sqlite"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64))


T_DDDEntityModel = typing.TypeVar('T_DDDEntityModel', bound=DDDEntityModel)


class DDDEntity(typing.Generic[T_DDDEntityModel]):
    """
    Base class for all domain entities. It requires a generic entity model as its persisted peer.

    Limitations:
    * typing.ClassVar does not yet support type variables so we might constrain it on the superclass
      but that then further confuses the type checker
    """
    model: typing.ClassVar
    repository: 'DDDRepository'
    is_aggregate_root: bool = False

    def __init__(self, name: str) -> None:
        if self.model is None:
            raise DDDException(code=500, msg='Misconfigured DDDEntity without model')
        self._uid: UniqueIdentifier = uuid.uuid4()
        self._name = name

    @property
    def uid(self) -> UniqueIdentifier:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @classmethod
    async def from_model(cls, model: T_DDDEntityModel) -> typing.Self:
        entity = cls(model.name)
        entity._uid = UniqueIdentifier(model.uid)
        return entity

    async def to_model(self) -> T_DDDEntityModel:
        model = self.model()
        model.uid = str(self._uid)
        model.name = self._name
        return model

    def __eq__(self, other: typing.Any) -> bool:
        return any([
            self.__class__ == other.__class__,
            self._uid == other.uid,
            self._name == other.name
        ])


T_DDDEntity = typing.TypeVar("T_DDDEntity", bound=DDDEntity)


class DDDAggregateRoot(DDDEntity[typing.Generic[T_DDDEntityModel]]):
    """
    Marker class for aggregate roots
    """
    is_aggregate_root: bool = True


class DDDRepository(typing.Generic[T_DDDEntity]):
    """
    Base class for all repositories

    Limitations:
    * typing.ClassVar does not yet support type variables so we might constrain it on the superclass
      but that then further confuses the type checker
    """
    entity: typing.ClassVar

    def __init__(self, session_maker: sqlalchemy.ext.asyncio.async_sessionmaker) -> None:
        if self.entity is None:
            raise DDDException(code=500, msg='Misconfigured DDDRepository without entity')
        self._session_maker = session_maker
        self._identity_map: typing.Dict[UniqueIdentifier, T_DDDEntity] = {}
        self.entity.repository = self

    async def get_by_uid(self, uid: UniqueIdentifier) -> T_DDDEntity:
        if uid in self._identity_map:
            return self._identity_map[uid]
        async with self._session_maker() as session:
            model = await session.get(self.entity.model, str(uid))
            if model is None:
                raise EntityNotFoundException()
            self._identity_map[uid] = await self.entity.from_model(model)
            return self._identity_map[uid]

    async def list(self) -> typing.List[T_DDDEntity]:
        async with self._session_maker() as session:
            models = await session.scalars(select(self.entity.model))
            return [await self.entity.from_model(m) for m in models]

    async def create(self, entity: T_DDDEntity) -> T_DDDEntity:
        async with self._session_maker() as session:
            async with session.begin():
                model = await entity.to_model()
                session.add(await entity.to_model())
            entity._uid = model.uid
            self._identity_map[entity.uid] = entity
        return self._identity_map[entity.uid]

    async def modify(self, entity: T_DDDEntity) -> T_DDDEntity:
        async with self._session_maker() as session:
            session.add(await entity.to_model())
        return entity

    async def remove(self, uid: UniqueIdentifier) -> None:
        async with self._session_maker() as session:
            model = await session.get(self.entity.model, str(uid))
            if model is None:
                raise EntityNotFoundException()
            await session.delete(model)
