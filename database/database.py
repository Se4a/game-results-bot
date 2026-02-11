from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import logging

logger = logging.getLogger(__name__)

# Создаем Base класс
Base = declarative_base()

# Импортируем все модели
from bot.models.user import User
from bot.models.subscription import Subscription
from bot.models.game_account import GameAccount
from bot.models.game_stats import GameSettings, PlayerStats
from bot.models.match import Match, MatchUpdate
from bot.models.daily_stats import DailyStats
from bot.models.payment import Payment

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info(f"Database initialized with URL: {database_url[:50]}...")
    
    async def create_tables(self):
        """Создать все таблицы в базе данных"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    
    async def drop_tables(self):
        """Удалить все таблицы (только для тестов!)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database tables dropped!")
    
    async def get_session(self) -> AsyncSession:
        """Получить сессию базы данных"""
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def execute_query(self, query):
        """Выполнить запрос и вернуть результат"""
        async with self.async_session() as session:
            try:
                result = await session.execute(query)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                logger.error(f"Database query error: {e}")
                raise
    
    async def close(self):
        """Закрыть соединение с базой данных"""
        await self.engine.dispose()
        logger.info("Database connection closed")