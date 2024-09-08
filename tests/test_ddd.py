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
import uuid
from mhpython.ddd import (
    EntityInvariantException,
    NodeEntity, EntityNotFoundException, ClusterEntity
)

@pytest.mark.asyncio
async def test_entity_invariant_exception():
    with pytest.raises(EntityInvariantException, match='\[400\] All nodes must belong to a cluster'):
        NodeEntity(name="test")
        assert False

@pytest.mark.asyncio
async def test_entity_notfound_exception(cluster_repository):
    with pytest.raises(EntityNotFoundException, match='\[404\] The specified entity does not exist'):
        await cluster_repository.get_by_uid(uuid.uuid4())
        assert False

@pytest.mark.asyncio
async def test_cluster_persistence(seed_clusters, cluster_repository):
    assert len(await cluster_repository.list()) == 10
    for cluster in seed_clusters:
        loaded = await cluster_repository.get_by_uid(cluster.uid)
        assert cluster.repository is not None
        assert loaded == cluster
        assert len(cluster.nodes) == 3
        for node in cluster.nodes:
            assert node.cluster == cluster

@pytest.mark.asyncio
async def test_cluster_lifecycle_via_repository(cluster_repository):
    cluster = await cluster_repository.create(ClusterEntity(name='Test Cluster'))
    assert cluster.uid is not None

    cluster.name = 'I changed my name'
    await cluster_repository.modify(cluster)

    loaded = await cluster_repository.get_by_uid(cluster.uid)
    assert loaded == cluster

    await cluster_repository.remove(cluster.uid)

@pytest.mark.asyncio
async def test_cluster_lifecycle_via_cluster(cluster_repository):
    cluster = ClusterEntity(name='Test Cluster')
    await cluster.save()

    cluster.name = 'I changed my name'
    await cluster.save()

    loaded = await cluster_repository.get_by_uid(cluster.uid)
    assert loaded == cluster

    await cluster.remove()
