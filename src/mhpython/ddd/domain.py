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

import pathlib
import typing

from mhpython.ddd import EntityInvariantException
from mhpython.ddd.base import DDDAggregateRoot
from mhpython.ddd.model import ClusterModel, NodeModel, NetworkModel, ImageModel


class ImageEntity(DDDAggregateRoot[ImageModel]):
    model = ImageModel

    def __init__(self, name: str, url: str) -> None:
        super().__init__(name)
        self._url = url
        self._path = pathlib.Path(__file__).parent.joinpath(f'{name}.img')

    @property
    def url(self) -> str:
        return self._url

    @property
    def path(self) -> pathlib.Path:
        return self._path

    def __eq__(self, other: typing.Any) -> bool:
        return all([
            super().__eq__(other),
            self._url == other.url,
            self._path == other.path,
        ])


class NetworkEntity(DDDAggregateRoot[NetworkModel]):
    model = NetworkModel

    def __init__(self, name: str, network: str, netmask: str, router: str):
        super().__init__(name)
        self._network = network
        self._netmask = netmask
        self._router = router

    @property
    def network(self) -> str:
        return self._network

    @property
    def netmask(self) -> str:
        return self._netmask

    @property
    def router(self) -> str:
        return self._router

    def __eq__(self, other: typing.Any) -> bool:
        return all([
            super().__eq__(other),
            self._network == other.network,
            self._netmask == other.netmask,
            self._router == other.router
        ])


class ClusterEntity(DDDAggregateRoot[ClusterModel]):
    model = ClusterModel

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._nodes: typing.List[NodeEntity] = []

    @property
    def nodes(self) -> typing.List['NodeEntity']:
        return self._nodes

    def add_node(self, node: 'NodeEntity') -> None:
        if self.dirty:
            raise EntityInvariantException(code=400, msg='You must save the cluster before adding nodes')
        if node in self._nodes:
            return
        if node.cluster is not None and node.cluster != self:
            # TODO: We may remove the node from the other cluster here instead of raising
            raise EntityInvariantException(code=400, msg='Node is a member of another cluster')
        node.cluster = self
        self._nodes.append(node)
        self._dirty = True

    def remove_node(self, node: 'NodeEntity') -> None:
        if node not in self._nodes or node.cluster != self:
            raise EntityInvariantException(code=400, msg='Node is not a member of this cluster')
        self._nodes.remove(node)
        self._dirty = True

    async def post_create(self) -> None:
        for node in self._nodes:
            await node.post_create()
        return await super().post_create()

    async def post_modify(self) -> None:
        for node in self._nodes:
            await node.post_modify()
        return await super().post_modify()

    def __eq__(self, other: typing.Any) -> bool:
        return all([
            super().__eq__(other),
            self._nodes == other.nodes,
            ])


class NodeEntity(DDDAggregateRoot[NodeModel]):
    model = NodeModel

    def __init__(self,
                 name: str,
                 network: NetworkEntity,
                 image: ImageEntity,
                 cluster: ClusterEntity | None = None) -> None:
        super().__init__(name)
        self._network = network
        self._image = image
        self._cluster = cluster

    @property
    def network(self) -> NetworkEntity:
        return self._network

    @property
    def image(self) -> ImageEntity:
        return self._image

    @property
    def cluster(self) -> ClusterEntity | None:
        return self._cluster

    @cluster.setter
    def cluster(self, cluster: ClusterEntity | None) -> None:
        if cluster is None and self._cluster is None:
            # We are already not associated with a cluster
            return
        elif cluster is None and self._cluster is not None:
            # We must remove ourselves from the cluster
            self._cluster.remove_node(self)
            self._cluster = None
        elif cluster is not None and self._cluster is not None and cluster.uid == self._cluster.uid:
            # We are already a member of this cluster
            return
        elif cluster is not None and self._cluster is not None and cluster.uid != self._cluster.uid:
            # We are a member of another cluster, which is currently not supported
            raise EntityInvariantException(code=400, msg='This node is already a member of another cluster')
        elif cluster is not None and self._cluster is None:
            # We will join this cluster
            self._cluster = cluster
            cluster.add_node(self)
        self._dirty = True

    async def post_create(self) -> None:
        if self._cluster is not None:
            self._cluster.dirty = False
        return await super().post_create()

    async def post_modify(self) -> None:
        if self._cluster is not None:
            self._cluster.dirty = False
        return await super().post_modify()

    def __eq__(self, other: typing.Any) -> bool:
        return all([
            super().__eq__(other),
            self._network == other.network,
            self._image == other.image,
            self._cluster == other.cluster
            ])
