from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database import Base

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_account_id = Column(Integer, ForeignKey('game_accounts.id'))
    game = Column(String(50))
    match_id = Column(String(255), unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # в секундах
    result = Column(String(50))  # 'win', 'loss', 'draw', 'ongoing'
    map = Column(String(100))
    mode = Column(String(100))
    
    # Игроки
    player_name = Column(String(255))
    player_team = Column(String(100))
    opponent_team = Column(String(100))
    
    # Основные показатели
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    kd_ratio = Column(Float, default=0.0)
    kda = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    
    # Дополнительные показатели
    adr = Column(Float, default=0.0)  # CS:GO/Valorant
    hs_percentage = Column(Float, default=0.0)
    mvp = Column(Integer, default=0)
    
    # Dota/LoL показатели
    gpm = Column(Float, default=0.0)
    xpm = Column(Float, default=0.0)
    last_hits = Column(Integer, default=0)
    denies = Column(Integer, default=0)
    hero_damage = Column(Integer, default=0)
    tower_damage = Column(Integer, default=0)
    healing = Column(Integer, default=0)
    net_worth = Column(Integer, default=0)
    
    # Valorant показатели
    acs = Column(Float, default=0.0)
    first_bloods = Column(Integer, default=0)
    plants = Column(Integer, default=0)
    defuses = Column(Integer, default=0)
    economy_rating = Column(Float, default=0.0)
    
    # WoT показатели
    wn8 = Column(Float, default=0.0)
    damage_dealt = Column(Integer, default=0)
    damage_assisted = Column(Integer, default=0)
    damage_blocked = Column(Integer, default=0)
    spotted = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    
    # PUBG показатели
    survival_time = Column(Float, default=0.0)
    walk_distance = Column(Float, default=0.0)
    drive_distance = Column(Float, default=0.0)
    longest_kill = Column(Float, default=0.0)
    headshot_kills = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    
    # Дополнительные данные
    raw_stats = Column(JSON)  # Полная статистика в JSON
    players_data = Column(JSON)  # Данные по всем игрокам
    is_tracked = Column(Boolean, default=False)  # Отслеживался ли матч
    is_completed = Column(Boolean, default=False)  # Завершен ли матч
    is_analyzed = Column(Boolean, default=False)  # Проанализирован ли AI
    ai_analysis = Column(JSON)  # AI анализ матча
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="match_history")
    game_account = relationship("GameAccount", back_populates="matches")
    updates = relationship("MatchUpdate", back_populates="match")
    
    @property
    def win_loss(self):
        """Текстовое представление результата"""
        if self.result == 'win':
            return 'Победа'
        elif self.result == 'loss':
            return 'Поражение'
        elif self.result == 'draw':
            return 'Ничья'
        else:
            return self.result
    
    @property
    def duration_formatted(self):
        """Форматированная длительность"""
        if not self.duration:
            return "N/A"
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def calculate_kda(self):
        """Рассчитать KDA"""
        if self.deaths > 0:
            self.kda = (self.kills + self.assists) / self.deaths
        else:
            self.kda = self.kills + self.assists
    
    def calculate_kd_ratio(self):
        """Рассчитать K/D"""
        if self.deaths > 0:
            self.kd_ratio = self.kills / self.deaths
        else:
            self.kd_ratio = self.kills
    
    def __repr__(self):
        return f"<Match(id={self.id}, game={self.game}, result={self.result}, player={self.player_name})>"


class MatchUpdate(Base):
    __tablename__ = 'match_updates'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    update_time = Column(DateTime, default=datetime.utcnow)
    game_time = Column(Integer)  # Время в матче (секунды)
    round = Column(Integer)  # Раунд (CS:GO/Valorant)
    player_stats = Column(JSON)  # Текущая статистика игрока
    team_stats = Column(JSON)  # Статистика команд
    events = Column(JSON)  # События в матче
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="updates")
    
    def __repr__(self):
        return f"<MatchUpdate(id={self.id}, match_id={self.match_id}, time={self.update_time})>"