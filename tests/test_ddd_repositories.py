import pytest
import pathlib
#
# from mhpython.ddd_repositories.base_types import BinaryScale, BinarySizedValue
# from mhpython.ddd_repositories.disks import DiskEntity, DiskEntityModel, DiskAggregateRoot, AsyncDiskAggregateRoot
#
#
# def test_disks(sync_session_maker):
#     aggregate_root = DiskAggregateRoot(model=DiskEntityModel, session_maker=sync_session_maker)
#
#     assert aggregate_root.list() == []
#     try:
#         disk = aggregate_root.create(DiskEntity(name='Test Disk',
#                                                 path=pathlib.Path(__file__).parent / 'build' / 'test.qcow2',
#                                                 size=BinarySizedValue(1, BinaryScale.G)))
#         loaded = aggregate_root.get(disk.id)
#         assert disk == loaded
#         disk.size = BinarySizedValue(2, scale=BinaryScale.G)
#         updated = aggregate_root.modify(disk)
#         assert disk == updated
#         listed = aggregate_root.list()
#         assert len(listed) == 1
#         assert disk == listed[0]
#     finally:
#         aggregate_root.remove(disk.id)
#         assert len(aggregate_root.list()) == 0
#         assert not disk.path.exists()
#
#
# @pytest.mark.asyncio(scope='module')
# async def test_async_disks(async_session_maker):
#     aggregate_root = AsyncDiskAggregateRoot(model=DiskEntityModel, session_maker=async_session_maker)
#     try:
#         disk = await aggregate_root.create(DiskEntity(name='Test Disk',
#                                                       path=pathlib.Path(__file__).parent / 'build' / 'test.qcow2',
#                                                       size=BinarySizedValue(1, BinaryScale.G)))
#         loaded = await aggregate_root.get(disk.id)
#         assert disk == loaded
#         disk.size = BinarySizedValue(2, scale=BinaryScale.G)
#         updated = await aggregate_root.modify(disk)
#         assert disk == updated
#         listed = await aggregate_root.list()
#         assert len(listed) == 1
#         assert disk == listed[0]
#     finally:
#         await aggregate_root.remove(disk.id)
#         assert len(await aggregate_root.list()) == 0
#         assert not disk.path.exists()
