import aiohttp
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from bot.config import config
import json

class RiotIntegration:
    """Интеграция с Riot Games API для Valorant и LoL"""
    
    def __init__(self):
        self.api_key = config.RIOT_API_KEY
        self.session = None
        self.regions = {
            'valorant': {
                'eu': 'eu',
                'na': 'na',
                'ap': 'ap',
                'kr': 'kr',
                'br': 'br',
                'latam': 'latam'
            },
            'lol': {
                'euw': 'euw1',
                'eune': 'eun1',
                'na': 'na1',
                'kr': 'kr',
                'br': 'br1',
                'lan': 'la1',
                'las': 'la2',
                'oce': 'oc1',
                'ru': 'ru',
                'tr': 'tr1',
                'jp': 'jp1'
            }
        }
    
    async def get_session(self):
        if not self.session:
            headers = {'X-Riot-Token': self.api_key}
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def get_valorant_account(self, riot_id: str, tag: str, region: str = 'eu') -> Dict:
        """Получить аккаунт Valorant"""
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag}"
        
        session = await self.get_session()
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
        return {}
    
    async def get_valorant_stats(self, puuid: str, region: str = 'eu') -> Dict:
        """Получить статистику Valorant"""
        # Получить последние матчи
        url = f"https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
        
        session = await self.get_session()
        async with session.get(url) as response:
            if response.status == 200:
                matches = await response.json()
                
                stats = {
                    'total_matches': len(matches),
                    'recent_matches': matches[:10],
                    'agents_played': {},
                    'maps_played': {}
                }
                
                # Анализируем матчи
                for match_id in matches[:5]:
                    match_url = f"https://{region}.api.riotgames.com/val/match/v1/matches/{match_id}"
                    async with session.get(match_url) as match_response:
                        if match_response.status == 200:
                            match_data = await match_response.json()
                            # Обрабатываем статистику
                            pass
                
                return stats
        return {}
    
    async def get_lol_account(self, riot_id: str, tag: str, region: str = 'euw1') -> Dict:
        """Получить аккаунт LoL"""
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag}"
        
        session = await self.get_session()
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
        return {}
    
    async def get_lol_stats(self, summoner_id: str, region: str = 'euw1') -> Dict:
        """Получить статистику LoL"""
        # Получить информацию о summoner
        summoner_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
        
        session = await self.get_session()
        async with session.get(summoner_url) as response:
            if response.status == 200:
                summoner_data = await response.json()
                
                # Получить ранги
                ranks_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
                async with session.get(ranks_url) as ranks_response:
                    if ranks_response.status == 200:
                        ranks_data = await ranks_response.json()
                    
                # Получить историю матчей
                matches_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_data['puuid']}/ids"
                params = {'count': 20}
                async with session.get(matches_url, params=params) as matches_response:
                    if matches_response.status == 200:
                        matches = await matches_response.json()
                
                stats = {
                    'summoner': summoner_data,
                    'ranks': ranks_data or [],
                    'recent_matches': matches or [],
                    'champion_stats': {},
                    'overall_stats': {}
                }
                
                return stats
        return {}
    
    async def close(self):
        """Закрыть сессию"""
        if self.session:
            await self.session.close()