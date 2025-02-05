from app.db import engine, AsyncSession, AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.models import Base
from app.__main__ import app
from starlette.testclient import TestClient
from typing import AsyncGenerator, Any

import pytest


@pytest.fixture(scope="function")
async def create_db() -> AsyncGenerator[Any | Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def db(create_db: AsyncGenerator[Any | Any]) -> AsyncIterator[async_sessionmaker]:
    async with AsyncSession() as session:
        yield session


@pytest.fixture
async def client() -> TestClient:
    client = TestClient(app)
    return client
