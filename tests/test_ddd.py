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
import mhpython.ddd.base
import mhpython.ddd.cluster
import mhpython.ddd.node

@pytest.mark.asyncio
async def test_cluster_persistence(async_session_maker):
    cluster_repository = mhpython.ddd.cluster.ClusterRepository(async_session_maker)
    clusters = []
    for i in range(0, 10):
        cluster = mhpython.ddd.cluster.ClusterEntity(name=f'Test Cluster {i}')
        for n in range(0, 5):
            node = mhpython.ddd.node.NodeEntity(name=f'Test Node {n}', cluster=cluster)
            cluster.nodes.append(node)
        await cluster_repository.create(cluster)
        assert cluster.uid is not None
        clusters.append(cluster)
    assert len(await cluster_repository.list()) == 10
    for cluster in clusters:
        loaded = await cluster_repository.get_by_uid(cluster.uid)
        assert loaded == cluster
