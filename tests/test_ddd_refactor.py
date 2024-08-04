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

import pytest
import typing
#
# from mhpython.ddd_refactor.base_types import (
#     UniqueIdentifier,
#     EntityModel, Entity,
#     AggregateRoot,
#     AsyncRepository)
#
# from sqlalchemy import String, Integer, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
#
# class DiskModel(EntityModel):
#     __tablename__ = 'disks'
#     name: Mapped[str] = mapped_column(String)
#     gb: Mapped[int] = mapped_column(Integer)
#
#
# class Disk(Entity[DiskModel]):
#
#     def __init__(self, name: str, gb: int) -> None:
#         super().__init__()
#         self._name = name
#         self._gb = gb
#
#     @property
#     def name(self) -> str:
#         return self._name
#
#     @property
#     def gb(self) -> int:
#         return self._gb
#
#     @staticmethod
#     def from_model(model: DiskModel) -> 'Disk':
#         entity = Disk(name=model.name, gb=model.gb)
#         entity._uid = UniqueIdentifier(model.uid)
#         return entity
#
#     def to_model(self, model: DiskModel | None = None) -> DiskModel:
#         if model is None:
#             return self.model_clazz(uid=str(self.uid),
#                                     name=self.name,
#                                     gb=self.gb)
#         else:
#             model.name = self.name
#             model.gb = self.gb
#
#     def validate(self) -> bool:
#         return all([
#             super().validate(),
#             self.name is not None,
#             self.gb > 0
#         ])
#
#
# class InstanceModel(EntityModel):
#     __tablename__ = 'instances'
#     name: Mapped[str] = mapped_column(String)
#     root_disk_uid: Mapped[str] = mapped_column(ForeignKey("disks.uid"), nullable=True)
#     root_disk: Mapped[DiskModel] = relationship("DiskModel", lazy='joined')
#
#
# class Instance(Entity[InstanceModel], AggregateRoot):
#
#     def __init__(self, name: str):
#         super().__init__()
#         self._name = name
#         self._root_disk: Disk | None = None
#         self._disks: typing.Set[Disk] = set()
#
#     @property
#     def name(self) -> str:
#         return self._name
#
#     @property
#     def root_disk(self) -> Disk | None:
#         return self._root_disk
#
#     @root_disk.setter
#     def root_disk(self, value: Disk | None) -> None:
#         self._root_disk = value
#
#     @staticmethod
#     def from_model(model: InstanceModel) -> 'Instance':
#         entity = Instance(name=model.name)
#         entity._uid = UniqueIdentifier(model.uid)
#         if model.root_disk is not None:
#             entity._root_disk = Disk.from_model(model.root_disk)
#         return entity
#
#     def to_model(self, model: DiskModel | None = None) -> InstanceModel:
#         if model is None:
#             model = self.model_clazz(uid=str(self.uid),
#                                      name=self.name,
#                                      root_disk_uid=None)
#         else:
#             model.name = self.name
#         if self.root_disk is not None:
#             model.root_disk_uid = str(self.root_disk.uid)
#         return model
#
#     def validate(self) -> bool:
#         return all([
#             super().validate(),
#             self.name is not None
#         ])
#
#
# class DiskRepository(AsyncRepository[Disk, DiskModel]):
#     pass
#
#
# class InstanceRepository(AsyncRepository[Instance, InstanceModel]):
#     pass
#
#
# @pytest.mark.asyncio
# async def test_refactor(async_session_maker):
#     disk_repository = DiskRepository(session_maker=async_session_maker,
#                                      entity_clazz=Disk,
#                                      model_clazz=DiskModel)
#     instance_repository = InstanceRepository(session_maker=async_session_maker,
#                                              entity_clazz=Instance,
#                                              model_clazz=InstanceModel)
#     assert await instance_repository.list() == []
#     assert await disk_repository.list() == []
#     disk = Disk(name='Root Disk', gb=5)
#     instance = Instance(name='Hello World')
#     try:
#         await instance_repository.create(instance)
#         assert instance.uid is not None
#         assert len(await instance_repository.list()) == 1
#
#         await disk_repository.create(disk)
#         assert disk.uid is not None
#
#         instance.root_disk = disk
#         await instance_repository.modify(instance)
#         assert instance.root_disk is not None
#         assert instance.root_disk.uid == disk.uid
#
#         loaded = await instance_repository.get_by_id(instance.uid)
#         assert loaded.uid == instance.uid
#         assert loaded.root_disk.uid == disk.uid
#     finally:
#         for instance in await instance_repository.list():
#             await instance_repository.remove(instance)
#         for disk in await disk_repository.list():
#             await disk_repository.remove(disk)
#         assert await disk_repository.list() == []
#         assert await instance_repository.list() == []
