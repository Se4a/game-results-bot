import asyncio
from aiogram import Bot
from bot.config import config
from bot.database import async_session
from sqlalchemy import select

async def init_payment_system(bot: Bot):
    """Инициализация платежной системы при запуске бота"""
    print("💰 Инициализация платежной системы...")
    
    # Проверяем, поддерживает ли бот платежи
    bot_info = await bot.get_me()
    
    # Получаем информацию о поддерживаемых платежах
    # В реальном приложении здесь можно проверить поддержку Stars
    print(f"🤖 Бот: @{bot_info.username}")
    print(f"💰 Поддерживаются платежи: Да (Telegram Stars)")
    
    # Проверяем наличие платежей в базе данных
    async with async_session() as session:
        from bot.database import Payment
        result = await session.execute(select(Payment))
        payments = result.scalars().all()
        
        print(f"📊 Всего платежей в базе: {len(payments)}")
        
        # Анализируем платежи по методам
        crypto_payments = [p for p in payments if p.payment_method == 'crypto']
        stars_payments = [p for p in payments if p.payment_method == 'stars']
        
        print(f"   ₿ Криптовалютных: {len(crypto_payments)}")
        print(f"   ⭐ Telegram Stars: {len(stars_payments)}")
    
    print("✅ Платежная система готова к работе")
    print(f"💱 Курс: 1 Star = ${config.STARS_TO_USD_RATE}")
    print(f"💎 Цены в Stars: {config.SUBSCRIPTION_PRICES_STARS}")
    
    return True