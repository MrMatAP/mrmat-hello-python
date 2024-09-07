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

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

import mhpython.ddd.base
import mhpython.ddd.cluster


class NodeModel(mhpython.ddd.base.DDDEntityModel):
    __tablename__ = 'nodes'
    cluster_uid: Mapped[str] = mapped_column(ForeignKey("clusters.uid"))


class NodeEntity(mhpython.ddd.base.DDDEntity[NodeModel]):
    model = NodeModel

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        if 'cluster' not in kwargs or kwargs['cluster'] is None:
            raise mhpython.ddd.base.EntityInvariantException(code=400, msg='All nodes must belong to a cluster')
        self._cluster: mhpython.ddd.cluster.ClusterEntity = kwargs['cluster']

    @property
    def cluster(self) -> 'mhpython.ddd.cluster.ClusterEntity':
        return self._cluster

    @classmethod
    async def from_model(cls, model: NodeModel, *args, **kwargs) -> typing.Self:
        entity = await super().from_model(model, *args, **kwargs)
        entity._name = model.name
        return entity

    async def to_model(self) -> NodeModel:
        model = await super().to_model()
        model.name = self._name
        model.cluster_uid = str(self._cluster.uid)
        return model


class NodeRepository(mhpython.ddd.base.DDDRepository[NodeEntity]):
    entity = NodeEntity
