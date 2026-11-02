from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)


engine = create_async_engine(
    DATABASE_URL,
)


SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db():

    async with SessionLocal() as db:
        yield db
