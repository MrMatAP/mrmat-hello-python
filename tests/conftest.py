import pathlib
import pytest
import pytest_asyncio

import sqlalchemy.orm
import sqlalchemy.ext.asyncio

from mhpython.ddd import DDDEntityModel


@pytest.fixture(scope='session')
def generics_db() -> pathlib.Path:
    db = pathlib.Path(__file__).parent.joinpath('build/ddd_repositories.sqlite')
    db.parent.mkdir(parents=True, exist_ok=True)
    yield db
    db.unlink(missing_ok=True)


@pytest.mark.asyncio
@pytest_asyncio.fixture
async def async_session_maker(generics_db) -> sqlalchemy.ext.asyncio.async_sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]:
    engine = sqlalchemy.ext.asyncio.create_async_engine(f'sqlite+aiosqlite:///{generics_db}', echo=False)
    asm = sqlalchemy.ext.asyncio.async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(DDDEntityModel.metadata.create_all)
    yield asm
    await engine.dispose()
