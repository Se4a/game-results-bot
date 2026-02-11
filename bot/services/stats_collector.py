import aiohttp
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from bot.config import config
import json

class GameStatsCollector:
    def __init__(self):
        self.session = None
        self.cache = {}
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def collect_stats(self, game: str, account_id: str, region: str = None) -> Dict:
        """Собирает статистику для конкретной игры"""
        
        collectors = {
            'csgo': self._collect_csgo_stats,
            'dota2': self._collect_dota_stats,
            'valorant': self._collect_valorant_stats,
            'lol': self._collect_lol_stats,
            'wot': self._collect_wot_stats,
            'pubg': self._collect_pubg_stats
        }
        
        collector = collectors.get(game)
        if not collector:
            return {}
        
        return await collector(account_id, region)
    
    async def _collect_csgo_stats(self, steam_id: str, region: str = None) -> Dict:
        """Собирает статистику CS:GO"""
        session = await self.get_session()
        
        # Используем Steam Web API и Faceit/ESEA API
        stats = {
            'game': 'csgo',
            'player_name': f'Player_{steam_id[-8:]}',
            'recent_matches': [],
            'overall_stats': {},
            'weapon_stats': {},
            'map_stats': {}
        }
        
        # Пример структуры данных для CS:GO
        stats['recent_matches'] = [
            {
                'match_id': f'csgo_{steam_id}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '35:22',
                'result': 'Win',
                'map': 'de_dust2',
                'kills': 25,
                'assists': 8,
                'deaths': 12,
                'kd_ratio': 2.08,
                'adr': 112,
                'hs_percentage': 45.2,
                'mvp': 3,
                'rating': 1.45,
                'score': 87,
                'team': 'CT',
                'economy': 14500
            }
        ]
        
        stats['overall_stats'] = {
            'total_matches': 1542,
            'wins': 832,
            'losses': 710,
            'win_rate': 54.0,
            'avg_kills': 21.4,
            'avg_deaths': 19.8,
            'avg_assists': 6.2,
            'avg_adr': 89.5,
            'avg_hs_percentage': 38.7,
            'total_mvp': 421,
            'rating': 1.12
        }
        
        return stats
    
    async def _collect_dota_stats(self, steam_id: str, region: str = None) -> Dict:
        """Собирает статистику Dota 2"""
        stats = {
            'game': 'dota2',
            'player_name': f'Player_{steam_id[-8:]}',
            'recent_matches': [],
            'overall_stats': {},
            'hero_stats': {},
            'role_stats': {}
        }
        
        # Данные для Dota 2
        stats['recent_matches'] = [
            {
                'match_id': f'dota_{steam_id}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '42:15',
                'result': 'Win',
                'hero': 'Invoker',
                'kills': 12,
                'deaths': 4,
                'assists': 18,
                'kda': 7.5,
                'gpm': 625,
                'xpm': 712,
                'last_hits': 312,
                'denies': 24,
                'hero_damage': 28500,
                'tower_damage': 4200,
                'healing': 0,
                'net_worth': 26500,
                'items': ['hand_of_midas', 'aghanims_scepter', 'boots_of_travel'],
                'role': 'Mid'
            }
        ]
        
        stats['overall_stats'] = {
            'total_matches': 2456,
            'wins': 1321,
            'losses': 1135,
            'win_rate': 53.8,
            'avg_kills': 8.2,
            'avg_deaths': 6.4,
            'avg_assists': 12.8,
            'avg_gpm': 512,
            'avg_xpm': 598,
            'avg_last_hits': 245,
            'mmr': 4520,
            'medal': 'Immortal'
        }
        
        return stats
    
    async def _collect_valorant_stats(self, riot_id: str, region: str = 'eu') -> Dict:
        """Собирает статистику Valorant"""
        stats = {
            'game': 'valorant',
            'player_name': riot_id.split('#')[0],
            'recent_matches': [],
            'overall_stats': {},
            'agent_stats': {},
            'weapon_stats': {}
        }
        
        # Данные для Valorant
        stats['recent_matches'] = [
            {
                'match_id': f'valorant_{hash(riot_id)}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '32:44',
                'result': 'Win',
                'map': 'Ascent',
                'agent': 'Jett',
                'kills': 28,
                'deaths': 14,
                'assists': 8,
                'acs': 312,
                'hs_percentage': 38.5,
                'first_bloods': 4,
                'plants': 2,
                'defuses': 1,
                'economy_rating': 85,
                'score': 7650,
                'combat_score': 245
            }
        ]
        
        stats['overall_stats'] = {
            'total_matches': 856,
            'wins': 467,
            'losses': 389,
            'win_rate': 54.6,
            'avg_kills': 18.2,
            'avg_deaths': 15.4,
            'avg_assists': 5.8,
            'avg_acs': 248,
            'avg_hs_percentage': 32.4,
            'rank': 'Diamond 2',
            'rr': 65
        }
        
        return stats
    
    async def _collect_lol_stats(self, riot_id: str, region: str = 'euw1') -> Dict:
        """Собирает статистику League of Legends"""
        stats = {
            'game': 'lol',
            'player_name': riot_id.split('#')[0],
            'recent_matches': [],
            'overall_stats': {},
            'champion_stats': {},
            'lane_stats': {}
        }
        
        # Данные для LoL
        stats['recent_matches'] = [
            {
                'match_id': f'lol_{hash(riot_id)}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '28:32',
                'result': 'Win',
                'champion': 'Yasuo',
                'kills': 12,
                'deaths': 3,
                'assists': 8,
                'kda': 6.67,
                'cs': 212,
                'cs_per_min': 7.4,
                'gold': 14500,
                'vision_score': 42,
                'damage': 28500,
                'damage_taken': 18500,
                'kill_participation': 72,
                'items': ['berserkers_greaves', 'immortal_shieldbow', 'infinity_edge'],
                'lane': 'Mid',
                'summoner_spells': ['Flash', 'Ignite']
            }
        ]
        
        stats['overall_stats'] = {
            'total_matches': 1845,
            'wins': 987,
            'losses': 858,
            'win_rate': 53.5,
            'avg_kills': 7.8,
            'avg_deaths': 5.6,
            'avg_assists': 8.4,
            'avg_cs_per_min': 6.9,
            'avg_vision_score': 38,
            'rank': 'Platinum I',
            'lp': 75,
            'main_role': 'Mid'
        }
        
        return stats
    
    async def _collect_wot_stats(self, account_id: str, region: str = 'ru') -> Dict:
        """Собирает статистику World of Tanks"""
        stats = {
            'game': 'wot',
            'player_name': f'Player_{account_id[-6:]}',
            'recent_battles': [],
            'overall_stats': {},
            'tank_stats': {},
            'nation_stats': {}
        }
        
        # Данные для WoT
        stats['recent_battles'] = [
            {
                'battle_id': f'wot_{account_id}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '7:24',
                'result': 'Win',
                'tank': 'Object 140',
                'tier': 10,
                'nation': 'USSR',
                'damage': 3850,
                'assisted_damage': 1240,
                'blocked_damage': 1850,
                'kills': 3,
                'spotted': 2,
                'xp': 985,
                'wn8': 2850,
                'survived': True,
                'credits': 45200,
                'map': 'Prokhorovka'
            }
        ]
        
        stats['overall_stats'] = {
            'total_battles': 12542,
            'wins': 6542,
            'losses': 5120,
            'draws': 880,
            'win_rate': 52.2,
            'avg_damage': 2450,
            'avg_kills': 1.8,
            'avg_xp': 745,
            'avg_wn8': 2150,
            'personal_rating': 8650,
            'max_damage': 11250,
            'max_kills': 9,
            'max_xp': 1850
        }
        
        return stats
    
    async def _collect_pubg_stats(self, account_id: str, region: str = 'steam') -> Dict:
        """Собирает статистику PUBG"""
        stats = {
            'game': 'pubg',
            'player_name': f'Player_{account_id[-8:]}',
            'recent_matches': [],
            'overall_stats': {},
            'weapon_stats': {},
            'map_stats': {}
        }
        
        # Данные для PUBG
        stats['recent_matches'] = [
            {
                'match_id': f'pubg_{account_id}_1',
                'date': datetime.now().strftime('%d.%m.%Y'),
                'duration': '24:32',
                'result': 'Top 3',
                'map': 'Erangel',
                'mode': 'Squad',
                'kills': 8,
                'assists': 2,
                'damage': 685,
                'headshot_kills': 3,
                'longest_kill': 312.5,
                'survival_time': 1420,
                'rank': 3,
                'walk_distance': 2850,
                'drive_distance': 1240,
                'heals': 4,
                'boosts': 3,
                'weapons': ['M416', 'Kar98k']
            }
        ]
        
        stats['overall_stats'] = {
            'total_matches': 856,
            'wins': 42,
            'top_10': 285,
            'avg_rank': 18.4,
            'avg_kills': 3.2,
            'avg_damage': 285,
            'avg_survival_time': 1250,
            'headshot_kill_ratio': 38.5,
            'most_kills': 14,
            'max_damage': 1850,
            'rank': 'Platinum II',
            'kd_ratio': 2.8
        }
        
        return stats
    
    async def get_player_stats_for_interval(
        self, 
        game: str, 
        account_id: str, 
        days: int = 30,
        region: str = None
    ) -> List[Dict]:
        """Получает статистику игрока за определенный период"""
        # В реальной реализации здесь будет запрос к API игр
        # Для примера возвращаем тестовые данные
        
        stats = await self.collect_stats(game, account_id, region)
        
        # Генерируем историю за указанный период
        history = []
        for i in range(min(days, 30)):
            match_date = datetime.now() - timedelta(days=i)
            
            base_match = stats['recent_matches'][0].copy() if stats['recent_matches'] else {}
            base_match['date'] = match_date.strftime('%d.%m.%Y')
            
            # Добавляем некоторую вариативность в статистику
            if 'kills' in base_match:
                base_match['kills'] = max(0, base_match['kills'] + (i % 5) - 2)
            if 'deaths' in base_match:
                base_match['deaths'] = max(1, base_match['deaths'] + (i % 3) - 1)
            
            history.append(base_match)
        
        return history
    
    async def close(self):
        """Закрывает сессию"""
        if self.session:
            await self.session.close()