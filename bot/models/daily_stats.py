from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from bot.database import Base

class DailyStats(Base):
    __tablename__ = 'daily_stats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    matches_used = Column(Integer, default=0)
    matches_tracked = Column(Integer, default=0)
    games_played = Column(JSON, default={})  # {game: count}
    last_match_time = Column(DateTime)
    last_reset = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="daily_stats")
    
    @property
    def is_today(self):
        """Статистика за сегодня?"""
        return self.date.date() == datetime.utcnow().date()
    
    def increment_matches(self, game: str = None):
        """Увеличить счетчик матчей"""
        self.matches_used += 1
        self.matches_tracked += 1
        
        if game:
            games = self.games_played or {}
            games[game] = games.get(game, 0) + 1
            self.games_played = games
        
        self.last_match_time = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def can_play_more(self, free_limit: int = 2, subscription_active: bool = False) -> bool:
        """Может ли пользователь играть больше матчей"""
        if subscription_active:
            return True
        return self.matches_used < free_limit
    
    def matches_left(self, free_limit: int = 2, subscription_active: bool = False) -> int:
        """Сколько матчей осталось"""
        if subscription_active:
            return float('inf')
        return max(0, free_limit - self.matches_used)
    
    def reset_daily(self):
        """Сбросить дневную статистику"""
        self.date = datetime.utcnow()
        self.matches_used = 0
        self.matches_tracked = 0
        self.games_played = {}
        self.last_reset = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<DailyStats(id={self.id}, user_id={self.user_id}, matches_used={self.matches_used})>"
