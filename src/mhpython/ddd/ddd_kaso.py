import typing
import uuid

from mhpython.ddd import (
    UniqueIdentifier,
    EntityNotFoundException,
    DDDAggregateRoot, DDDEntity, DDDEntityModel, T_DDDEntityModel, DDDRepository
)

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column


class ClusterModel(DDDEntityModel):
    __tablename__ = 'clusters'
    name: Mapped[str] = mapped_column(String, unique=True)


class Cluster(DDDAggregateRoot[ClusterModel]):

    def __init__(self, model_clazz: typing.Type[ClusterModel]) -> None:
        super().__init__(model_clazz=model_clazz)
        self._name = f'Cluster {uuid.uuid4()}'
        self._nodes: typing.List['Node'] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def add_node(self, node: 'Node') -> None:
        node.cluster = self
        self._nodes.append(node)

    def remove_node(self, node: 'Node') -> None:
        node.cluster = None
        self._nodes.remove(node)

    @classmethod
    async def from_model(cls, model: ClusterModel) -> typing.Self:
        entity = await super().from_model(model)
        entity._name = model.name
        return entity

    async def to_model(self) -> ClusterModel:
        model = await super().to_model()
        model.name = self._name
        return model


class ClusterRepository(DDDRepository[Cluster]):
    pass


class NodeModel(DDDEntityModel):
    __tablename__ = 'nodes'
    name: Mapped[str] = mapped_column(String, unique=True)
    cluster_uid: Mapped[str] = mapped_column(UUID(as_uuid=True).with_variant(String(32), "sqlite"))


class Node(DDDEntity[NodeModel]):

    def __init__(self, model_clazz: typing.Type[NodeModel]) -> None:
        super().__init__(model_clazz)
        self._name = f'Node {uuid.uuid4()}'
        self._cluster: Cluster | None = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def cluster(self) -> Cluster | None:
        return self._cluster

    @cluster.setter
    def cluster(self, cluster: Cluster):
        self._cluster = cluster

    @classmethod
    async def from_model(cls, model: NodeModel) -> typing.Self:
        entity = await super().from_model(model)
        entity._name = model.name
        return entity

    async def to_model(self) -> NodeModel:
        model = await super().to_model()
        model.name = self._name
        return model
