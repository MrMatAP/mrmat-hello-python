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

import uuid
import pydantic

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .base_types import ORMBase


class DDDPersonSampleSchema(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, description='A unique identity for this endity')
    name: str = pydantic.Field(description='The entity name')


class DDDPersonSampleORM(ORMBase):
    __tablename__ = 'ddd_person_sample'
    id: Mapped[str] = mapped_column(UUID(as_uuid=True).with_variant(String(32), 'sqlite'), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class DDDPersonSample:

    _schema_class = DDDPersonSampleSchema
    _orm_class = DDDPersonSampleORM

    def __init__(self, session_maker: async_sessionmaker[AsyncSession], name: str, id: uuid.UUID = None):
        self._session_maker = session_maker
        self._schema = DDDPersonSampleSchema(name=name)
        self._orm = DDDPersonSampleORM(name=name)
        # Synchronisation doesn't work yet
        self._synchronise()

    def _synchronise(self):
        for field in self._schema.model_fields.keys():
            setattr(self._orm, field, getattr(self._schema, field))

    @property
    def id(self) -> uuid.UUID:
        return self._schema.id

    @property
    def name(self) -> str:
        return self._schema.name

    async def persist(self):
        async with self._session_maker() as session:
            session.add(self._orm)
            await session.commit()

    @staticmethod
    async def get_by_id(session_maker: async_sessionmaker[AsyncSession], id: uuid.UUID) -> 'DDDPersonSample':
        async with session_maker() as session:
            model = await session.get(DDDPersonSample._orm_class, str(id))
            if model is None:
                raise ValueError(f"No such entity with this id")
            return model
