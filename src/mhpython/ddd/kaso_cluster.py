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

import typing
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mhpython.ddd import DDDEntityModel, DDDAggregateRoot, DDDRepository


class ClusterModel(DDDEntityModel):
    __tablename__ = 'clusters'
    name: Mapped[str] = mapped_column(String, unique=True)


class ClusterEntity(DDDAggregateRoot[ClusterModel]):
    model = ClusterModel

    def __init__(self) -> None:
        super().__init__()
        self._name = f'Cluster {uuid.uuid4()}'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @classmethod
    async def from_model(cls, model: ClusterModel) -> typing.Self:
        entity = await super().from_model(model)
        entity._name = model.name
        return entity

    async def to_model(self) -> ClusterModel:
        model = await super().to_model()
        model.name = self._name
        return model

    def __eq__(self, other: typing.Any) -> bool:
        return any([
            super.__eq__(self, other),
            self._name == other.name,
        ])

class ClusterRepository(DDDRepository[ClusterEntity]):
    entity = ClusterEntity
