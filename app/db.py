from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import AsyncIterator
from app.settings import settings

async_engine = create_async_engine(
    f"{settings.DB_URI}/{settings.DB_NAME}",
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    yield AsyncSessionLocal


AsyncSession = async_sessionmaker
