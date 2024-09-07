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

from sqlalchemy.orm import Mapped, relationship

import mhpython.ddd.base
import mhpython.ddd.node


class ClusterModel(mhpython.ddd.base.DDDEntityModel):
    """
    Domain model of a cluster
    IMPORTANT: Relationships must not be loaded lazily. See
    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads
    """
    __tablename__ = 'clusters'
    nodes: Mapped[typing.List[mhpython.ddd.node.NodeModel]] = relationship(cascade='all, delete-orphan', lazy='selectin')


class ClusterEntity(mhpython.ddd.base.DDDAggregateRoot[ClusterModel]):
    model = ClusterModel

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self._nodes: typing.List[mhpython.ddd.node.NodeEntity] = []

    @property
    def nodes(self) -> typing.List[mhpython.ddd.node.NodeEntity]:
        return self._nodes

    @classmethod
    async def from_model(cls, model: ClusterModel, *args, **kwargs) -> typing.Self:
        entity = await super().from_model(model, *args, **kwargs)
        entity._nodes = [await mhpython.ddd.node.NodeEntity.from_model(n, cluster=entity) for n in model.nodes]
        return entity

    async def to_model(self) -> ClusterModel:
        model = await super().to_model()
        model.nodes = [await n.to_model() for n in self._nodes]
        return model

    def __eq__(self, other: typing.Any) -> bool:
        return any([
            super.__eq__(self, other),
            self._name == other.name,
        ])

class ClusterRepository(mhpython.ddd.base.DDDRepository[ClusterEntity]):
    entity = ClusterEntity
