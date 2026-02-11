"""
Integrations package initialization
"""

from .steam_integration import SteamIntegration
from .riot_integration import RiotIntegration
from .wot_integration import WoTIntegration
from .pubg_integration import PUBGIntegration

class GameIntegrations:
    def __init__(self):
        self.steam = SteamIntegration()
        self.riot = RiotIntegration()
        self.wot = WoTIntegration()
        self.pubg = PUBGIntegration()
    
    async def get_integration_for_game(self, game: str):
        """Получить интеграцию для игры"""
        integrations = {
            'csgo': self.steam,
            'dota2': self.steam,
            'valorant': self.riot,
            'lol': self.riot,
            'wot': self.wot,
            'pubg': self.pubg
        }
        return integrations.get(game)
    
    async def close_all(self):
        """Закрыть все сессии"""
        await self.steam.close()
        await self.riot.close()
        await self.wot.close()
        await self.pubg.close()

__all__ = [
    'SteamIntegration',
    'RiotIntegration',
    'WoTIntegration',
    'PUBGIntegration',
    'GameIntegrations'
]