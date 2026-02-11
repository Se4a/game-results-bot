from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from bot.database import Base

class GameAccount(Base):
    __tablename__ = 'game_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game = Column(String(50))  # 'csgo', 'dota2', 'valorant', 'lol', 'wot', 'pubg'
    account_id = Column(String(255))
    nickname = Column(String(255))
    region = Column(String(50))
    is_primary = Column(Boolean, default=True)
    last_updated = Column(DateTime)
    last_changed = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="game_accounts")
    settings = relationship("GameSettings", back_populates="game_account", uselist=False)
    matches = relationship("Match", back_populates="game_account")
    
    @property
    def can_be_changed(self):
        """Можно ли изменить аккаунт (прошло ли 48 часов)"""
        if not self.last_changed:
            return True
        
        time_diff = datetime.utcnow() - self.last_changed
        return time_diff.total_seconds() >= 48 * 3600
    
    @property
    def hours_until_change(self):
        """Сколько часов осталось до возможности смены"""
        if not self.last_changed:
            return 0
        
        time_diff = datetime.utcnow() - self.last_changed
        if time_diff.total_seconds() >= 48 * 3600:
            return 0
        
        remaining = (48 * 3600) - time_diff.total_seconds()
        return round(remaining / 3600, 1)
    
    def update_nickname(self, new_nickname: str):
        """Обновить никнейм"""
        self.nickname = new_nickname
        self.last_updated = datetime.utcnow()
    
    def __repr__(self):
        return f"<GameAccount(id={self.id}, game={self.game}, nickname={self.nickname})>"
