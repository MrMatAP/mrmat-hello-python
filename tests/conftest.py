import pathlib
import pytest
import pytest_asyncio

import sqlalchemy.orm
import sqlalchemy.ext.asyncio
from mhpython.ddd_repositories.base_types import ORMBase


@pytest.fixture(scope='session')
def generics_db() -> pathlib.Path:
    db = pathlib.Path(__file__).parent.joinpath('build/ddd_repositories.sqlite')
    db.parent.mkdir(parents=True, exist_ok=True)
    return db


@pytest.fixture(scope='module')
def generics_session_maker(generics_db) -> sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]:
    engine = sqlalchemy.create_engine(f'sqlite:///{generics_db}', echo=False)
    session_maker = sqlalchemy.orm.sessionmaker(engine, expire_on_commit=False)
    with engine.begin() as conn:
        ORMBase.metadata.create_all(conn)
    yield session_maker
    engine.dispose()


@pytest.mark.asyncio
@pytest_asyncio.fixture
async def generics_async_session_maker(generics_db) -> sqlalchemy.ext.asyncio.async_sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]:
    engine = sqlalchemy.ext.asyncio.create_async_engine(f'sqlite+aiosqlite:///{generics_db}', echo=False)
    async_session = sqlalchemy.ext.asyncio.async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(ORMBase.metadata.create_all)
    yield async_session
    await engine.dispose()
