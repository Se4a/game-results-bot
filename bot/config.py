import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "*8335049265:AAGjWzldB1DV6nsdFwMekC_YZsEdtkrlzWc*")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database/bot.db")
    
    # API Keys
    STEAM_API_KEY = os.getenv("STEAM_API_KEY", "*7DA945B46467DE86A1E0534DCA5F4790*")
    WOT_APPLICATION_ID = os.getenv("WOT_APPLICATION_ID", "*your_wot_app_id*")
    RIOT_API_KEY = os.getenv("RIOT_API_KEY", "*your_riot_api_key*")
    PUBG_API_KEY = os.getenv("PUBG_API_KEY", "*your_pubg_api_key*")
    
    # Payment
    CRYPTO_ADDRESS = os.getenv("CRYPTO_ADDRESS", "*TB3gXVXXb7ueq1siwuSNoLD7yXg6g7ByDJ*")
    ZERO_CRYPTO_PAY_API_KEY = os.getenv("ZERO_CRYPTO_PAY_API_KEY", "*your_zerocryptopay_key*")
    
    # Redis for caching and timers
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Limits
    FREE_MATCHES_PER_DAY = 2
    DEFAULT_COMPARE_DEPTH = 3
    MAX_COMPARE_DEPTH = 20
    ACCOUNT_CHANGE_COOLDOWN = 48  # hours
    
    # Update intervals
    STATS_UPDATE_INTERVAL = 180  # seconds
    SUBSCRIPTION_CHECK_INTERVAL = 3600  # seconds
    
    # Webhook settings (for Render)
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
    WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    
    # Webapp settings
    WEBAPP_HOST = "0.0.0.0"
    WEBAPP_PORT = int(os.getenv("PORT", 5000))
    
    # Admin IDs
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(','))) if os.getenv("ADMIN_IDS") else []
    
    # Telegram Stars pricing (1 Star = $0.01, 100 Stars = $1.00)
    STARS_TO_USD_RATE = 0.01
    
    # Subscription prices in Stars
    SUBSCRIPTION_PRICES_STARS = {
        '1_month': 99,      # $0.99
        '3_months': 250,    # $2.50
        '6_months': 500,    # $5.00
        '12_months': 1000   # $10.00
    }
    
    # Subscription prices in USD
    SUBSCRIPTION_PRICES_USD = {
        '1_month': 0.99,
        '3_months': 2.50,
        '6_months': 5.00,
        '12_months': 10.00
    }
    
    # Subscription durations in days
    SUBSCRIPTION_DURATIONS = {
        '1_month': 30,
        '3_months': 90,
        '6_months': 180,
        '12_months': 365
    }
    
    # Game-specific update intervals (seconds)
    UPDATE_INTERVALS = {
    'csgo': 60,      # Steam API ограничения
    'dota2': 30,     # OpenDota API - 60 запросов/мин
    'valorant': 45,  # Riot API - 20 запросов/сек, 100/2мин
    'lol': 60,       # Riot API - те же ограничения
    'wot': 20,       # Wargaming API - 10 запросов/сек
    'pubg': 120      # PUBG API - 10 запросов/мин
    }

    # Max requests per minute for each API
    API_RATE_LIMITS = {
    'steam': 100,        # 100 запросов/мин
    'opendota': 60,      # 60 запросов/мин
    'riot': 100,         # 100 запросов/2мин
    'wargaming': 600,    # 10 запросов/сек = 600/мин
    'pubg_api': 10       # 10 запросов/мин
    }
    
config = Config()