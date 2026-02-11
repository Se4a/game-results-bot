import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from datetime import datetime

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info(f"Database initialized with URL: {database_url[:50]}...")

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database tables dropped!")

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def close(self):
        await self.engine.dispose()
        logger.info("Database connection closed")

# ---------- Глобальный экземпляр для импорта async_session ----------
def _get_global_db():
    from bot.config import config
    return Database(config.DATABASE_URL)

# Создаём глобальный экземпляр БД
db = _get_global_db()

# Экспортируем async_session для удобного импорта в хендлерах
async_session = db.async_session

__all__ = [
    'Base',
    'Database',
    'async_session',
    'db'
]
