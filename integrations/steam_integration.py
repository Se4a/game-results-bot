import aiohttp
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from bot.config import config
import json

class SteamIntegration:
    """Интеграция с Steam API для CS:GO и Dota 2"""
    
    def __init__(self):
        self.api_key = config.STEAM_API_KEY
        self.base_url = "https://api.steampowered.com"
        self.session = None
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def verify_steam_account(self, steam_id: str) -> Dict:
        """Проверить Steam аккаунт"""
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v2/"
        params = {
            'key': self.api_key,
            'steamids': steam_id
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                players = data.get('response', {}).get('players', [])
                if players:
                    return players[0]
        return {}
    
    async def get_csgo_stats(self, steam_id: str) -> Dict:
        """Получить статистику CS:GO"""
        url = f"{self.base_url}/ISteamUserStats/GetUserStatsForGame/v2/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'appid': 730  # CS:GO app ID
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('playerstats', {}).get('stats', [])
        return []
    
    async def get_dota_stats(self, steam_id: str) -> Dict:
        """Получить статистику Dota 2"""
        url = f"{self.base_url}/ISteamUserStats/GetUserStatsForGame/v2/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'appid': 570  # Dota 2 app ID
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('playerstats', {}).get('stats', [])
        return []
    
    async def get_recent_matches(self, steam_id: str, game: str, count: int = 10) -> List[Dict]:
        """Получить последние матчи"""
        if game == 'dota2':
            # Используем OpenDota API для Dota 2
            url = f"https://api.opendota.com/api/players/{steam_id}/matches"
            params = {'limit': count}
            
            session = await self.get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        elif game == 'csgo':
            # Для CS:GO используем сторонние API или Game Coordinator
            # Временно возвращаем тестовые данные
            return [
                {
                    'match_id': f'csgo_{steam_id}_1',
                    'start_time': int(datetime.now().timestamp()) - 3600,
                    'duration': 2100,
                    'result': 'win',
                    'kills': 25,
                    'deaths': 12,
                    'assists': 8
                }
            ]
        
        return []
    
    async def get_friends_list(self, steam_id: str) -> List[Dict]:
        """Получить список друзей"""
        url = f"{self.base_url}/ISteamUser/GetFriendList/v1/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'relationship': 'friend'
        }
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('friendslist', {}).get('friends', [])
        return []
    
    async def close(self):
        """Закрыть сессию"""
        if self.session:
            await self.session.close()