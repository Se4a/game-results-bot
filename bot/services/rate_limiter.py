import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Ограничитель запросов к API"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.limits = {
            'steam': {'per_minute': 100, 'per_second': 2},
            'opendota': {'per_minute': 60, 'per_second': 1},
            'riot': {'per_minute': 50, 'per_second': 0.5},  # 100/2мин
            'wargaming': {'per_minute': 600, 'per_second': 10},
            'pubg': {'per_minute': 10, 'per_second': 0.2}
        }
    
    async def wait_if_needed(self, api: str):
        """Подождать если превышен лимит"""
        
        if api not in self.limits:
            return
        
        now = datetime.now()
        limit = self.limits[api]
        
        # Очищаем старые запросы
        self.requests[api] = [
            req_time for req_time in self.requests[api]
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Проверяем лимит в минуту
        if len(self.requests[api]) >= limit['per_minute']:
            # Находим самый старый запрос
            oldest = min(self.requests[api])
            wait_time = 60 - (now - oldest).total_seconds()
            if wait_time > 0:
                logger.info(f"Rate limit for {api}, waiting {wait_time:.1f} sec")
                await asyncio.sleep(wait_time)
        
        # Проверяем лимит в секунду
        recent_requests = [
            req_time for req_time in self.requests[api]
            if now - req_time < timedelta(seconds=1)
        ]
        
        if len(recent_requests) >= limit['per_second']:
            wait_time = 1 - (now - min(recent_requests)).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Добавляем текущий запрос
        self.requests[api].append(now)
    
    def get_api_for_game(self, game: str) -> str:
        """Получить тип API для игры"""
        mapping = {
            'csgo': 'steam',
            'dota2': 'opendota',
            'valorant': 'riot',
            'lol': 'riot',
            'wot': 'wargaming',
            'pubg': 'pubg'
        }
        return mapping.get(game, 'default')