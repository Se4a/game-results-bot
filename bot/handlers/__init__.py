from .start import register_start_handlers
from .games.csgo import register_csgo_handlers
from .games.dota import register_dota_handlers
# from .games.valorant import register_valorant_handlers
# from .games.lol import register_lol_handlers
# from .games.wot import register_wot_handlers
# from .games.pubg import register_pubg_handlers
from .subscription import register_subscription_handlers
from .settings import register_settings_handlers
from .admin import register_admin_handlers
from .payment import register_payment_handlers
from .complete_stats import register_complete_stats_handlers

def register_all_handlers(dp):
    register_start_handlers(dp)
    register_csgo_handlers(dp)
    register_dota_handlers(dp)
    # register_valorant_handlers(dp)
    # register_lol_handlers(dp)
    # register_wot_handlers(dp)
    # register_pubg_handlers(dp)
    register_subscription_handlers(dp)
    register_settings_handlers(dp)
    register_admin_handlers(dp)
    register_payment_handlers(dp)
    register_complete_stats_handlers(dp)
