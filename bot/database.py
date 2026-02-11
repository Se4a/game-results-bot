from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey, BigInteger
from datetime import datetime, timedelta
import pytz

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255))
    language = Column(String(10), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    game_accounts = relationship("GameAccount", back_populates="user")
    match_history = relationship("Match", back_populates="user")
    daily_stats = relationship("DailyStats", back_populates="user")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    is_active = Column(Boolean, default=False)
    plan_type = Column(String(50))  # 'monthly', '3months', '6months', 'yearly'
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    payment_method = Column(String(50))  # 'crypto', 'telegram_stars'
    transaction_id = Column(String(255))
    
    # Relationships
    user = relationship("User", back_populates="subscription")

class GameAccount(Base):
    __tablename__ = 'game_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game = Column(String(50))  # 'csgo', 'dota2', 'valorant', 'lol', 'wot', 'pubg'
    account_id = Column(String(255))
    nickname = Column(String(255))
    region = Column(String(50))
    last_updated = Column(DateTime)
    last_changed = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="game_accounts")
    settings = relationship("GameSettings", back_populates="game_account", uselist=False)

class GameSettings(Base):
    __tablename__ = 'game_settings'
    
    id = Column(Integer, primary_key=True)
    game_account_id = Column(Integer, ForeignKey('game_accounts.id'), unique=True)
    compare_depth = Column(Integer, default=3)
    auto_update = Column(Boolean, default=True)
    notifications = Column(Boolean, default=True)
    
    # Relationships
    game_account = relationship("GameAccount", back_populates="settings")

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game = Column(String(50))
    match_id = Column(String(255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    result = Column(String(50))  # 'win', 'loss', 'draw'
    duration = Column(Integer)  # in seconds
    stats = Column(JSON)  # JSON with all match statistics
    is_tracked = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="match_history")

class DailyStats(Base):
    __tablename__ = 'daily_stats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    matches_used = Column(Integer, default=0)
    last_reset = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="daily_stats")

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    currency = Column(String(10))
    plan_type = Column(String(50))
    status = Column(String(50))  # 'pending', 'completed', 'failed'
    transaction_id = Column(String(255))
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime)

# Database engine and session
class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session