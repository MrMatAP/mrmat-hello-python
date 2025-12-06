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

import uuid

import pytest
from mhpython.ddd.base import (
    EntityNotFoundException,
    EntityInvariantException,
)
from mhpython.ddd.domain import ClusterEntity


@pytest.mark.asyncio
async def test_entity_not_found_exception(node_repository):
    """
    Test whether an attempt to get an entity that doesn't exist raises
    """
    with pytest.raises(
        EntityNotFoundException,
        match='\\[404\\] The specified entity does not exist',
    ):
        await node_repository.get_by_uid(uuid.uuid4())
        assert False


@pytest.mark.asyncio
async def test_node_persistence(seed_nodes, node_repository):
    """
    Test whether nodes can be persisted
    """
    assert len(await node_repository.list()) == 3
    for node in seed_nodes:
        loaded = await node_repository.get_by_uid(node.uid)
        assert node.repository is not None
        assert loaded == node
        assert node.network is not None
        assert node.image is not None


@pytest.mark.asyncio
async def test_add_set_cluster_on_node(seed_nodes, node_repository, cluster_repository):
    """
    Test whether we can set a cluster on a node
    """
    loaded_node = await node_repository.get_by_uid(seed_nodes[0].uid)
    assert loaded_node.cluster is None

    cluster = await ClusterEntity(name='Test Cluster').save()
    loaded_node.cluster = cluster
    assert cluster.dirty
    assert loaded_node.dirty
    await loaded_node.save()
    assert not loaded_node.dirty
    assert not cluster.dirty

    updated_node = await node_repository.get_by_uid(loaded_node.uid)
    assert updated_node.cluster == cluster
    assert updated_node in cluster.nodes
    assert not updated_node.dirty
    assert not cluster.dirty

    updated_cluster = await cluster_repository.get_by_uid(cluster.uid)
    assert updated_node in updated_cluster.nodes
    assert not updated_cluster.dirty


@pytest.mark.asyncio
async def test_add_node_to_cluster(seed_nodes, node_repository, cluster_repository):
    """
    Test whether we can add a node to a cluster
    """
    node = seed_nodes[0]
    cluster = await ClusterEntity(name='Test Cluster').save()
    cluster.add_node(node)
    assert cluster.dirty
    assert node.dirty
    assert await cluster.save()
    assert not cluster.dirty
    assert not node.dirty


@pytest.mark.asyncio
async def test_move_node_to_another_cluster(
    seed_nodes, node_repository, cluster_repository
):
    """
    Test whether we can move a node from one cluster to another
    """
    node = await node_repository.get_by_uid(seed_nodes[0].uid)
    assert node.cluster is None

    cluster1 = await ClusterEntity(name='Test Cluster 1').save()
    node.cluster = cluster1
    await node.save()

    cluster2 = await ClusterEntity(name='Test Cluster 2').save()
    with pytest.raises(
        EntityInvariantException,
        match='\\[400\\] This node is already a member of another cluster',
    ):
        node.cluster = cluster2


@pytest.mark.asyncio
async def test_add_node_to_dirty_cluster(
    seed_nodes, node_repository, cluster_repository
):
    """
    Test whether adding a node to a dirty cluster raises
    """
    node = await node_repository.get_by_uid(seed_nodes[0].uid)
    assert node.cluster is None
    assert not node.dirty

    cluster = ClusterEntity(name='Test Cluster')
    assert cluster.dirty
    with pytest.raises(
        EntityInvariantException,
        match='\\[400\\] You must save the cluster before adding nodes',
    ):
        cluster.add_node(node)


@pytest.mark.asyncio
async def test_rename_cluster(cluster_repository):
    """
    Test whether a cluster can be renamed
    """
    cluster = await ClusterEntity(name='Test Cluster').save()
    cluster.name = 'I renamed myself'
    assert cluster.dirty
    await cluster.save()
    assert not cluster.dirty

    loaded = await cluster_repository.get_by_uid(cluster.uid)
    assert not loaded.dirty
    assert loaded == cluster
