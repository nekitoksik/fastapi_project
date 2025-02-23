from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,  # Размер пула
    max_overflow=20,  # Максимальное количество соединений сверх pool_size
    pool_timeout=30,  # Таймаут ожидания свободного соединения
    pool_recycle=3600,
)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
