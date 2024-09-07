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

from mhpython.ddd.base import DDDAggregateRoot, DDDEntity, EntityInvariantException
from mhpython.ddd.model import ClusterModel, NodeModel


class ClusterEntity(DDDAggregateRoot[ClusterModel]):
    model = ClusterModel

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self._nodes: typing.List[NodeEntity] = []

    @property
    def nodes(self) -> typing.List['NodeEntity']:
        return self._nodes

    @classmethod
    async def from_model(cls, model: ClusterModel, *args, **kwargs) -> typing.Self:
        entity = await super().from_model(model, *args, **kwargs)
        entity._nodes = [await NodeEntity.from_model(n, cluster=entity) for n in model.nodes]
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


class NodeEntity(DDDEntity[NodeModel]):
    model = NodeModel

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        if 'cluster' not in kwargs or kwargs['cluster'] is None:
            raise EntityInvariantException(code=400, msg='All nodes must belong to a cluster')
        self._cluster: ClusterEntity = kwargs['cluster']

    @property
    def cluster(self) -> ClusterEntity:
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
