from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database import Base

class GameSettings(Base):
    __tablename__ = 'game_settings'
    
    id = Column(Integer, primary_key=True)
    game_account_id = Column(Integer, ForeignKey('game_accounts.id'), unique=True)
    compare_depth = Column(Integer, default=3)  # Глубина сравнения (N игр)
    auto_update = Column(Boolean, default=True)  # Автообновление в live
    notifications = Column(Boolean, default=True)  # Уведомления
    update_interval = Column(Integer, default=180)  # Интервал обновления (сек)
    detailed_stats = Column(Boolean, default=True)  # Подробная статистика
    ai_analysis = Column(Boolean, default=True)  # AI анализ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    game_account = relationship("GameAccount", back_populates="settings")
    
    def __repr__(self):
        return f"<GameSettings(id={self.id}, game_account_id={self.game_account_id}, compare_depth={self.compare_depth})>"


class PlayerStats(Base):
    __tablename__ = 'player_stats'
    
    id = Column(Integer, primary_key=True)
    game_account_id = Column(Integer, ForeignKey('game_accounts.id'))
    match_id = Column(String(255))
    game = Column(String(50))
    stats_date = Column(DateTime)
    stats_type = Column(String(50))  # 'overall', 'recent', 'season', 'lifetime'
    
    # Общая статистика
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    # CS:GO/Dota/Valorant/LoL статистика
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    kd_ratio = Column(Float, default=0.0)
    kda = Column(Float, default=0.0)
    adr = Column(Float, default=0.0)  # Average Damage per Round
    hs_percentage = Column(Float, default=0.0)
    mvp = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # Dota/LoL специфичные
    gpm = Column(Float, default=0.0)  # Gold Per Minute
    xpm = Column(Float, default=0.0)  # XP Per Minute
    last_hits = Column(Integer, default=0)
    denies = Column(Integer, default=0)
    hero_damage = Column(Integer, default=0)
    tower_damage = Column(Integer, default=0)
    healing = Column(Integer, default=0)
    net_worth = Column(Integer, default=0)
    
    # Valorant специфичные
    acs = Column(Float, default=0.0)  # Average Combat Score
    first_bloods = Column(Integer, default=0)
    plants = Column(Integer, default=0)
    defuses = Column(Integer, default=0)
    economy_rating = Column(Float, default=0.0)
    
    # WoT специфичные
    wn8 = Column(Float, default=0.0)
    avg_damage = Column(Float, default=0.0)
    avg_kills = Column(Float, default=0.0)
    avg_xp = Column(Float, default=0.0)
    spotted = Column(Integer, default=0)
    assisted_damage = Column(Integer, default=0)
    blocked_damage = Column(Integer, default=0)
    
    # PUBG специфичные
    survival_time = Column(Float, default=0.0)
    walk_distance = Column(Float, default=0.0)
    drive_distance = Column(Float, default=0.0)
    longest_kill = Column(Float, default=0.0)
    headshot_kills = Column(Integer, default=0)
    
    # Дополнительные метрики
    raw_stats = Column(JSON)  # JSON со всей статистикой
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game_account = relationship("GameAccount", back_populates="stats")
    
    def calculate_win_rate(self):
        """Рассчитать винрейт"""
        if self.matches_played > 0:
            self.win_rate = (self.wins / self.matches_played) * 100
        else:
            self.win_rate = 0.0
    
    def calculate_kda(self):
        """Рассчитать KDA"""
        if self.deaths > 0:
            self.kda = (self.kills + self.assists) / self.deaths
        else:
            self.kda = self.kills + self.assists
    
    def __repr__(self):
        return f"<PlayerStats(id={self.id}, game={self.game}, win_rate={self.win_rate:.1f}%)>"