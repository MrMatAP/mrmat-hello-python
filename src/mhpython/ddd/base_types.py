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

from sqlalchemy import UUID, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

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


T_DDDEntityModel = typing.TypeVar('T_DDDEntityModel', bound=DDDEntityModel)


class DDDEntity(typing.Generic[T_DDDEntityModel]):
    """
    Base class for all domain entities. It requires a generic entity model as its persisted peer.
    """

    def __init__(self, model_clazz: typing.Type[T_DDDEntityModel]) -> None:
        self._uid: UniqueIdentifier = uuid.uuid4()
        self._model_clazz: typing.Type[T_DDDEntityModel] = model_clazz

    @property
    def uid(self) -> UniqueIdentifier:
        return self._uid

    @property
    def model_clazz(self) -> typing.Type[T_DDDEntityModel]:
        return self._model_clazz

    @classmethod
    async def from_model(cls, model: T_DDDEntityModel) -> typing.Self:
        entity = cls(model_clazz=model.__class__)
        entity._uid = UniqueIdentifier(model.uid)
        return entity

    async def to_model(self) -> T_DDDEntityModel:
        model = self._model_clazz()
        model.uid = str(self._uid)
        return model


T_DDDEntity = typing.TypeVar("T_DDDEntity", bound=DDDEntity)


class DDDAggregateRoot(DDDEntity[T_DDDEntityModel]):
    """
    Base class for all aggregate roots.
    This is just a subclass of DDDEntity, but allows type checking
    """


T_DDDAggregateRoot = typing.TypeVar('T_DDDAggregateRoot', bound=DDDAggregateRoot)


class DDDRepository(typing.Generic[T_DDDAggregateRoot]):
    """
    Base class for all repositories
    """

    def __init__(self,
                 session_maker: async_sessionmaker[AsyncSession],
                 entity_clazz: typing.Type[T_DDDAggregateRoot]) -> None:
        self._session_maker = session_maker
        self._entity_clazz: typing.Type[T_DDDAggregateRoot] = entity_clazz
        self._model_clazz = entity_clazz.model_clazz
        self._identity_map: typing.Dict[UniqueIdentifier, T_DDDAggregateRoot] = {}

    async def get_by_uid(self, uid: UniqueIdentifier) -> T_DDDAggregateRoot:
        if uid in self._identity_map:
            return self._identity_map[uid]
        async with self._session_maker() as session:
            model = await session.get(self._model_clazz, str(uid))
            if model is None:
                raise EntityNotFoundException()
            self._identity_map[uid] = await self._entity_clazz.from_model(model)
            return self._identity_map[uid]

    async def list(self) -> typing.List[T_DDDAggregateRoot]:
        async with self._session_maker() as session:
            models = await session.scalars(select(self._model_clazz))
            return [await self._model_clazz.from_model(m) for m in models]

    async def create(self, entity: T_DDDAggregateRoot) -> T_DDDAggregateRoot:
        async with self._session_maker() as session:
            async with session.begin():
                model = await entity.to_model()
                session.add(await entity.to_model())
            entity._uid = model.uid
            self._identity_map[entity.uid] = entity
        return self._identity_map[entity.uid]

    async def modify(self, entity: T_DDDAggregateRoot) -> T_DDDAggregateRoot:
        async with self._session_maker() as session:
            session.add(await entity.to_model())
        return entity

    async def remove(self, uid: UniqueIdentifier) -> None:
        async with self._session_maker() as session:
            model = await session.get(self._model_clazz, str(uid))
            if model is None:
                raise EntityNotFoundException()
            await session.delete(model)
