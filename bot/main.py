import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.config import config
from bot.database import Database
from bot.handlers import register_all_handlers
from bot.utils.timers import start_timers
from bot.services.notification_service import NotificationService
from bot.services.live_updater import LiveMatchUpdater
from database.init_db import init_database
from database.ensure_admin import ensure_infinite_subscription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup(dp: Dispatcher):
    """Действия при запуске бота"""
    logger.info("Бот запускается...")
    
    # Инициализируем базу данных и создаем бесконечную подписку для @terentiev_v
    await init_database()
    
    # Обеспечиваем бесконечную подписку для @terentiev_v
    from database.ensure_admin import ensure_infinite_subscription
    await ensure_infinite_subscription()
    
    # Инициализируем платежную систему
    from services.payment_initializer import init_payment_system
    await init_payment_system(dp.bot)
    
    # Устанавливаем команды бота
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("stats", "Моя статистика"),
        types.BotCommand("subscription", "Моя подписка"),
        types.BotCommand("admin", "Админ-панель")
    ])
    
    logger.info("Бот успешно запущен!")

async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # Initialize database
    db = Database(config.DATABASE_URL)
    await db.create_tables()
    
    # Register middlewares
    dp.middleware.setup(LoggingMiddleware())
    
    # Register all handlers
    register_all_handlers(dp)
    
    # Initialize services
    notification_service = NotificationService(bot)
    live_updater = LiveMatchUpdater(bot)
    
    # Store services in dispatcher for access in handlers
    dp['live_updater'] = live_updater
    dp['stats_collector'] = ExtendedStatsCollector()
    
    # Set startup handler
    dp.register_startup_handler(on_startup)
    
    # Start background tasks
    asyncio.create_task(start_timers(bot, db))
    
    print("🤖 Бот запускается...")
    print(f"🎮 Поддерживаемые игры: {list(config.GAME_METRICS.keys())}")
    print(f"⏱️ Интервалы обновления: {live_updater.update_intervals}")
    print("✅ Все системы готовы!")
    
    # Start polling (for development)
    try:
        await dp.start_polling()
    finally:
        # Cleanup
        await live_updater.cleanup()
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())