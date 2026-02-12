from .csgo import register_csgo_handlers
from .dota import register_dota_handlers
from .valorant import register_valorant_handlers
from .lol import register_lol_handlers
from .wot import register_wot_handlers
from .pubg import register_pubg_handlers

__all__ = [
    'register_csgo_handlers',
    'register_dota_handlers',
    'register_valorant_handlers',
    'register_lol_handlers',
    'register_wot_handlers',
    'register_pubg_handlers'
]
