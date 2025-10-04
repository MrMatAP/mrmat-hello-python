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

import pytest
import pytest_asyncio
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

import mhpython.ddd.base
from mhpython.ddd import NodeEntity
from mhpython.ddd.domain import ImageEntity, NetworkEntity
from mhpython.ddd.repository import (
    ImageRepository,
    NetworkRepository,
    NodeRepository,
    ClusterRepository,
)


@pytest.fixture(scope="session")
def generics_db() -> pathlib.Path:
    db = pathlib.Path(__file__).parent.parent.joinpath(
        "build/ddd_repositories.sqlite"
    )
    db.parent.mkdir(parents=True, exist_ok=True)
    yield db
    db.unlink(missing_ok=True)


@pytest_asyncio.fixture
async def async_session_maker(
    generics_db,
) -> sqlalchemy.ext.asyncio.async_sessionmaker[
    sqlalchemy.ext.asyncio.AsyncSession
]:
    engine = sqlalchemy.ext.asyncio.create_async_engine(
        f"sqlite+aiosqlite:///{generics_db}", echo=False
    )
    asm = sqlalchemy.ext.asyncio.async_sessionmaker(
        engine, expire_on_commit=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(mhpython.ddd.base.DDDModel.metadata.create_all)
    yield asm
    await engine.dispose()


@pytest_asyncio.fixture
async def image_repository(async_session_maker) -> ImageRepository:
    return ImageRepository(async_session_maker)


@pytest_asyncio.fixture
async def network_repository(async_session_maker) -> NetworkRepository:
    return NetworkRepository(async_session_maker)


@pytest_asyncio.fixture
async def node_repository(async_session_maker) -> NodeRepository:
    return NodeRepository(async_session_maker)


@pytest_asyncio.fixture
async def cluster_repository(async_session_maker) -> ClusterRepository:
    return ClusterRepository(async_session_maker)


@pytest_asyncio.fixture
async def seed_images(image_repository) -> typing.List[ImageEntity]:
    images: typing.List[ImageEntity] = []
    for i in range(0, 3):
        image = await image_repository.create(
            ImageEntity(f"Image {i}", url="https://image.url/{i}.img")
        )
        images.append(image)
    yield images
    for image in images:
        await image_repository.remove(image)


@pytest_asyncio.fixture(scope="function")
async def seed_networks(network_repository) -> typing.List[NetworkEntity]:
    networks: typing.List[NetworkEntity] = [
        await NetworkEntity(
            name="Host-only Network",
            network="172.16.0.0",
            netmask="255.255.255.0",
            router="172.16.0.1",
        ).save(),
        await NetworkEntity(
            name="NAT Network",
            network="172.16.1.0",
            netmask="255.255.255.0",
            router="172.16.1.1",
        ).save(),
        await NetworkEntity(
            name="Bridged Network",
            network="172.16.2.0",
            netmask="255.255.255.0",
            router="172.16.2.1",
        ).save(),
    ]
    yield networks
    for network in networks:
        await network_repository.remove(network)


@pytest_asyncio.fixture(scope="function")
async def seed_nodes(
    node_repository, seed_images, seed_networks
) -> typing.List[NodeEntity]:
    nodes: typing.List[NodeEntity] = []
    for i in range(0, 3):
        node = await node_repository.create(
            NodeEntity(
                name=f"Node-{i}", network=seed_networks[0], image=seed_images[0]
            )
        )
        nodes.append(node)
    yield nodes
    for node in nodes:
        await node_repository.remove(node)
