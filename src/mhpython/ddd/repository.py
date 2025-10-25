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

from mhpython.ddd.base import DDDRepository
from mhpython.ddd.domain import (
    ImageEntity,
    NetworkEntity,
    ClusterEntity,
    NodeEntity,
)
from mhpython.ddd.model import ImageModel, NetworkModel, ClusterModel, NodeModel


class ImageRepository(DDDRepository[ImageEntity, ImageModel]):
    entity_class = ImageEntity
    model_class = ImageModel

    @classmethod
    async def from_model(cls, model: ImageModel, *args, **kwargs) -> ImageEntity:
        kwargs['url'] = model.url
        entity = await super().from_model(model, *args, **kwargs)
        entity._path = pathlib.Path(model.path)
        return entity

    @classmethod
    async def to_model(
        cls, entity: ImageEntity, persisted: ImageModel | None = None
    ) -> ImageModel:
        model = await super().to_model(entity, persisted)
        model.url = entity.url
        model.path = str(entity.path)
        return model


class NetworkRepository(DDDRepository[NetworkEntity, NetworkModel]):
    entity_class = NetworkEntity
    model_class = NetworkModel

    @classmethod
    async def from_model(cls, model: NetworkModel, *args, **kwargs) -> NetworkEntity:
        kwargs['network'] = model.network
        kwargs['netmask'] = model.netmask
        kwargs['router'] = model.router
        entity = await super().from_model(model, *args, **kwargs)
        return entity

    @classmethod
    async def to_model(
        cls, entity: NetworkEntity, persisted: NetworkModel | None = None
    ) -> NetworkModel:
        model = await super().to_model(entity, persisted)
        model.network = entity.network
        model.netmask = entity.netmask
        model.router = entity.router
        return model


class ClusterRepository(DDDRepository[ClusterEntity, ClusterModel]):
    entity_class = ClusterEntity
    model_class = ClusterModel

    @classmethod
    async def from_model(cls, model: ClusterModel, *args, **kwargs) -> ClusterEntity:
        entity = await super().from_model(model, *args, **kwargs)
        return entity

    @classmethod
    async def to_model(
        cls, entity: ClusterEntity, persisted: ClusterModel | None = None
    ) -> ClusterModel:
        model = await super().to_model(entity, persisted)
        return model


class NodeRepository(DDDRepository[NodeEntity, NodeModel]):
    entity_class = NodeEntity
    model_class = NodeModel

    @classmethod
    async def from_model(cls, model: NodeModel, *args, **kwargs) -> NodeEntity:
        kwargs['network'] = await NetworkRepository.from_model(model.network)
        kwargs['image'] = await ImageRepository.from_model(model.image)
        entity = await super().from_model(model, *args, **kwargs)
        entity._network = await NetworkRepository.from_model(model.network)
        if model.cluster_uid is not None:
            entity._cluster = await ClusterRepository.from_model(model.cluster)
        return entity

    @classmethod
    async def to_model(
        cls, entity: NodeEntity, persisted: NodeModel | None = None
    ) -> NodeModel:
        model = await super().to_model(entity, persisted)
        model.network_uid = str(entity.network.uid)
        model.image_uid = str(entity.image.uid)
        if entity.cluster is not None:
            model.cluster_uid = str(entity.cluster.uid)
        return model
