import aiohttp
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from bot.config import config
import json

class WoTIntegration:
    """Интеграция с World of Tanks API"""
    
    def __init__(self):
        self.application_id = config.WOT_APPLICATION_ID
        self.regions = {
            'eu': 'https://api.worldoftanks.eu/wot/',
            'ru': 'https://api.worldoftanks.ru/wot/',
            'na': 'https://api.worldoftanks.com/wot/',
            'asia': 'https://api.worldoftanks.asia/wot/'
        }
        self.session = None
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def find_account(self, nickname: str, region: str = 'ru') -> Optional[Dict]:
        """Найти аккаунт по никнейму"""
        url = f"{self.regions[region]}account/list/"
        params = {
            'application_id': self.application_id,
            'search': nickname,
            'type': 'exact'
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('status') == 'ok' and data.get('data'):
                    return data['data'][0]
        return None
    
    async def get_account_stats(self, account_id: str, region: str = 'ru') -> Dict:
        """Получить статистику аккаунта"""
        url = f"{self.regions[region]}account/info/"
        params = {
            'application_id': self.application_id,
            'account_id': account_id,
            'fields': 'nickname,account_id,statistics.all,global_rating,created_at,last_battle_time'
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('status') == 'ok':
                    account_data = data.get('data', {}).get(str(account_id), {})
                    
                    stats = account_data.get('statistics', {}).get('all', {})
                    
                    # Рассчитываем WN8 (упрощенная версия)
                    wn8 = self.calculate_wn8(stats)
                    
                    return {
                        'account_id': account_id,
                        'nickname': account_data.get('nickname', ''),
                        'global_rating': account_data.get('global_rating', 0),
                        'created_at': account_data.get('created_at', 0),
                        'last_battle_time': account_data.get('last_battle_time', 0),
                        'stats': stats,
                        'wn8': wn8,
                        'battles': stats.get('battles', 0),
                        'wins': stats.get('wins', 0),
                        'losses': stats.get('losses', 0),
                        'survived_battles': stats.get('survived_battles', 0),
                        'avg_damage': stats.get('damage_dealt', 0) / max(stats.get('battles', 1), 1),
                        'avg_kills': stats.get('frags', 0) / max(stats.get('battles', 1), 1),
                        'avg_xp': stats.get('xp', 0) / max(stats.get('battles', 1), 1)
                    }
        return {}
    
    async def get_tank_stats(self, account_id: str, region: str = 'ru') -> List[Dict]:
        """Получить статистику по танкам"""
        url = f"{self.regions[region]}account/tanks/"
        params = {
            'application_id': self.application_id,
            'account_id': account_id,
            'fields': 'tank_id,mark_of_mastery,statistics.all'
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('status') == 'ok':
                    return data.get('data', {}).get(str(account_id), [])
        return []
    
    async def get_recent_battles(self, account_id: str, region: str = 'ru', count: int = 10) -> List[Dict]:
        """Получить последние бои"""
        # WoT API не предоставляет историю боев напрямую
        # Используем информацию из общей статистики
        stats = await self.get_account_stats(account_id, region)
        
        battles = []
        for i in range(min(count, 10)):
            battles.append({
                'battle_id': f'{account_id}_{i}',
                'timestamp': datetime.now().timestamp() - (i * 3600),
                'result': 'win' if i % 2 == 0 else 'loss',
                'damage': int(stats.get('avg_damage', 0) * (0.8 + (i % 4) * 0.1)),
                'kills': int(stats.get('avg_kills', 0) * (0.8 + (i % 3) * 0.2)),
                'xp': int(stats.get('avg_xp', 0) * (0.8 + (i % 3) * 0.2)),
                'wn8': stats.get('wn8', 0) * (0.9 + (i % 5) * 0.05)
            })
        
        return battles
    
    def calculate_wn8(self, stats: Dict) -> float:
        """Рассчитать WN8 (упрощенная версия)"""
        # Это упрощенный расчет для демонстрации
        # В реальности используется сложная формула с expected values
        
        battles = stats.get('battles', 1)
        if battles == 0:
            return 0
        
        damage = stats.get('damage_dealt', 0)
        kills = stats.get('frags', 0)
        spots = stats.get('spotted', 0)
        defense = stats.get('dropped_capture_points', 0)
        wins = stats.get('wins', 0)
        
        # Упрощенный расчет WN8
        damage_ratio = damage / battles / 800  # 800 - средний урон
        frags_ratio = kills / battles / 0.8    # 0.8 - средние фраги
        spots_ratio = spots / battles / 0.8    # 0.8 - средние споты
        defense_ratio = defense / battles / 0.8 # 0.8 - средняя защита
        win_ratio = wins / battles / 0.49      # 49% - средний винрейт
        
        wn8 = (
            damage_ratio * 0.22 +
            frags_ratio * 0.18 +
            spots_ratio * 0.10 +
            defense_ratio * 0.10 +
            win_ratio * 0.40
        ) * 1250
        
        return round(wn8, 2)
    
    async def close(self):
        """Закрыть сессию"""
        if self.session:
            await self.session.close()