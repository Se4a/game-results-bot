from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database import Base

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
    payments = relationship("Payment", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, telegram_id={self.telegram_id})>"