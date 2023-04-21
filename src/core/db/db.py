from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.settings import settings

engine = create_async_engine(settings.database_url)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
