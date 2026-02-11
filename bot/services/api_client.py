import aiohttp
import asyncio
from datetime import datetime
from bot.config import config
import json

class SteamAPIClient:
    def __init__(self):
        self.base_url = "https://api.steampowered.com"
        self.api_key = config.STEAM_API_KEY
    
    async def verify_steam_account(self, steam_id: str) -> bool:
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v2/"
        params = {
            'key': self.api_key,
            'steamids': steam_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return bool(data.get('response', {}).get('players', []))
        return False
    
    async def get_csgo_matches(self, steam_id: str, limit: int = 3) -> list:
        # Note: Steam Web API doesn't provide direct CS:GO match history
        # This would require using other services or the Game Coordinator
        # For now, return mock data
        return [
            {
                'match_id': f'csgo_{steam_id[-8:]}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '35:22',
                'result': 'Win',
                'player_stats': {
                    'name': f'Player_{steam_id[-4:]}',
                    'kills': 25,
                    'assists': 8,
                    'deaths': 12,
                    'kd': 2.08,
                    'adr': 112,
                    'hs_percent': 45.2,
                    'mvp': 3
                },
                'avg_kda': '1.85',
                'avg_adr': '98.5'
            }
        ]

class WoTAPIClient:
    def __init__(self):
        self.regions = {
            'eu': 'https://api.worldoftanks.eu/wot/',
            'ru': 'https://api.worldoftanks.ru/wot/',
            'na': 'https://api.worldoftanks.com/wot/',
            'asia': 'https://api.worldoftanks.asia/wot/'
        }
        self.app_id = config.WOT_APPLICATION_ID
    
    async def verify_account(self, account_id: str, region: str = 'eu') -> dict:
        url = f"{self.regions.get(region)}account/info/"
        params = {
            'application_id': self.app_id,
            'account_id': account_id,
            'fields': 'nickname,account_id'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'ok':
                        return data.get('data', {}).get(str(account_id), {})
        return {}
    
    async def get_player_stats(self, account_id: str, region: str = 'eu') -> dict:
        url = f"{self.regions.get(region)}account/info/"
        params = {
            'application_id': self.app_id,
            'account_id': account_id,
            'fields': 'statistics.all,global_rating'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'ok':
                        return data.get('data', {}).get(str(account_id), {})
        return {}

class RiotAPIClient:
    def __init__(self):
        self.api_key = config.RIOT_API_KEY
        self.base_urls = {
            'valorant': 'https://{}.api.riotgames.com',
            'lol': 'https://{}.api.riotgames.com/lol'
        }
    
    async def verify_account(self, game: str, username: str, tag: str, region: str) -> dict:
        if game == 'valorant':
            url = f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}"
            headers = {'Authorization': self.api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
        
        return {}

class PUBGAPIClient:
    def __init__(self):
        self.api_key = config.PUBG_API_KEY
        self.base_url = "https://api.pubg.com"
    
    async def verify_account(self, player_name: str, platform: str = 'steam') -> dict:
        url = f"{self.base_url}/shards/{platform}/players"
        params = {'filter[playerNames]': player_name}
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/vnd.api+json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
        return {}