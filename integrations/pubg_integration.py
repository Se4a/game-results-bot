import aiohttp
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from bot.config import config
import json

class PUBGIntegration:
    """Интеграция с PUBG API"""
    
    def __init__(self):
        self.api_key = config.PUBG_API_KEY
        self.session = None
        self.platforms = ['steam', 'xbox', 'psn', 'kakao']
        self.base_url = "https://api.pubg.com/shards"
    
    async def get_session(self):
        if not self.session:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/vnd.api+json'
            }
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def find_player(self, player_name: str, platform: str = 'steam') -> Optional[Dict]:
        """Найти игрока по имени"""
        url = f"{self.base_url}/{platform}/players"
        params = {'filter[playerNames]': player_name}
        
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('data'):
                    return data['data'][0]
        return None
    
    async def get_player_stats(self, player_id: str, platform: str = 'steam', season_id: str = None) -> Dict:
        """Получить статистику игрока"""
        if not season_id:
            # Получить текущий сезон
            seasons_url = f"{self.base_url}/{platform}/seasons"
            session = await self.get_session()
            
            async with session.get(seasons_url) as response:
                if response.status == 200:
                    seasons_data = await response.json()
                    for season in seasons_data.get('data', []):
                        if season.get('attributes', {}).get('isCurrentSeason'):
                            season_id = season['id']
                            break
            
            if not season_id:
                return {}
        
        # Получить статистику сезона
        stats_url = f"{self.base_url}/{platform}/players/{player_id}/seasons/{season_id}"
        
        async with session.get(stats_url) as response:
            if response.status == 200:
                data = await response.json()
                
                # Обрабатываем статистику
                stats = {
                    'player_id': player_id,
                    'season_id': season_id,
                    'game_mode_stats': {},
                    'overall_stats': {},
                    'recent_matches': []
                }
                
                # Извлекаем статистику по режимам
                game_mode_stats = data.get('data', {}).get('attributes', {}).get('gameModeStats', {})
                stats['game_mode_stats'] = game_mode_stats
                
                # Рассчитываем общую статистику
                total_matches = 0
                total_wins = 0
                total_kills = 0
                total_damage = 0
                
                for mode, mode_stats in game_mode_stats.items():
                    total_matches += mode_stats.get('roundsPlayed', 0)
                    total_wins += mode_stats.get('wins', 0)
                    total_kills += mode_stats.get('kills', 0)
                    total_damage += mode_stats.get('damageDealt', 0)
                
                stats['overall_stats'] = {
                    'total_matches': total_matches,
                    'total_wins': total_wins,
                    'total_kills': total_kills,
                    'total_damage': total_damage,
                    'win_rate': (total_wins / max(total_matches, 1)) * 100,
                    'avg_kills': total_kills / max(total_matches, 1),
                    'avg_damage': total_damage / max(total_matches, 1),
                    'kd_ratio': total_kills / max(total_matches - total_wins, 1)
                }
                
                return stats
        return {}
    
    async def get_match_history(self, player_id: str, platform: str = 'steam', count: int = 10) -> List[Dict]:
        """Получить историю матчей"""
        # Сначала получаем данные игрока
        player_url = f"{self.base_url}/{platform}/players/{player_id}"
        
        session = await self.get_session()
        async with session.get(player_url) as response:
            if response.status == 200:
                player_data = await response.json()
                match_ids = player_data.get('data', {}).get('relationships', {}).get('matches', {}).get('data', [])
                
                matches = []
                for match_data in match_ids[:count]:
                    match_id = match_data.get('id')
                    match_info = await self.get_match_details(match_id, platform)
                    if match_info:
                        matches.append(match_info)
                
                return matches
        return []
    
    async def get_match_details(self, match_id: str, platform: str = 'steam') -> Optional[Dict]:
        """Получить детали матча"""
        url = f"{self.base_url}/{platform}/matches/{match_id}"
        
        session = await self.get_session()
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                match_info = {
                    'match_id': match_id,
                    'created_at': data.get('data', {}).get('attributes', {}).get('createdAt', ''),
                    'duration': data.get('data', {}).get('attributes', {}).get('duration', 0),
                    'game_mode': data.get('data', {}).get('attributes', {}).get('gameMode', ''),
                    'map_name': data.get('data', {}).get('attributes', {}).get('mapName', ''),
                    'participants': [],
                    'telemetry_url': None
                }
                
                # Получаем участников
                included = data.get('included', [])
                for item in included:
                    if item.get('type') == 'participant':
                        participant = item.get('attributes', {})
                        match_info['participants'].append({
                            'name': participant.get('stats', {}).get('name', ''),
                            'player_id': participant.get('stats', {}).get('playerId', ''),
                            'rank': participant.get('stats', {}).get('winPlace', 0),
                            'kills': participant.get('stats', {}).get('kills', 0),
                            'damage': participant.get('stats', {}).get('damageDealt', 0),
                            'survival_time': participant.get('stats', {}).get('timeSurvived', 0)
                        })
                    elif item.get('type') == 'asset':
                        match_info['telemetry_url'] = item.get('attributes', {}).get('URL')
                
                return match_info
        return None
    
    async def close(self):
        """Закрыть сессию"""
        if self.session:
            await self.session.close()