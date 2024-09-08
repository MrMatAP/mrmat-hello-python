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
import pathlib
import pytest
import pytest_asyncio

import sqlalchemy.orm
import sqlalchemy.ext.asyncio

import mhpython.ddd.base
from mhpython.ddd import ClusterRepository, ClusterEntity, NodeEntity

@pytest.fixture(scope='session')
def generics_db() -> pathlib.Path:
    db = pathlib.Path(__file__).parent.parent.joinpath('build/ddd_repositories.sqlite')
    db.parent.mkdir(parents=True, exist_ok=True)
    yield db
    db.unlink(missing_ok=True)

@pytest.mark.asyncio
@pytest_asyncio.fixture
async def async_session_maker(generics_db) -> sqlalchemy.ext.asyncio.async_sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]:
    engine = sqlalchemy.ext.asyncio.create_async_engine(f'sqlite+aiosqlite:///{generics_db}', echo=False)
    asm = sqlalchemy.ext.asyncio.async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(mhpython.ddd.base.DDDModel.metadata.create_all)
    yield asm
    await engine.dispose()

@pytest.mark.asyncio
@pytest_asyncio.fixture
async def cluster_repository(async_session_maker) -> ClusterRepository:
    yield ClusterRepository(async_session_maker)

@pytest.mark.asyncio
@pytest_asyncio.fixture
async def seed_clusters(cluster_repository) -> typing.List[ClusterEntity]:
    clusters: typing.List[ClusterEntity] = []
    for c in range(0, 10):
        cluster = await cluster_repository.create(ClusterEntity(f'Cluster {c}'))
        for n in range(0, 3):
            await cluster.add_node(NodeEntity(name=f'Node {n}', cluster=cluster))
        clusters.append(cluster)
    yield clusters
    for cluster in clusters:
        await cluster_repository.remove(cluster.uid)