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

from mhpython.ddd.ddd_kaso import (
    ClusterRepository, Cluster, ClusterModel,
    Node, NodeModel
)


@pytest.mark.asyncio
async def test_clusters(async_session_maker):
    cluster_repository = ClusterRepository(session_maker=async_session_maker,
                                           entity_clazz=Cluster)
    assert cluster_repository is not None
    clusters = []
    for i in range(1, 10):
        cluster = Cluster(model_clazz=ClusterModel)
        cluster.name = f'Test Cluster {i}'
        await cluster_repository.create(cluster)
        assert cluster.uid is not None
        clusters.append(cluster)

    for cluster in clusters:
        for i in range(1, 10):
            node = Node(model_clazz=NodeModel)
            node.name = f'Test Node {i}'
            cluster.add_node(node)
        await cluster_repository.modify(cluster)
    pass
