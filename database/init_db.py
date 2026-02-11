import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database import Database, User, Subscription
from bot.config import config
from datetime import datetime, timedelta

async def init_database():
    """Initialize database with admin user"""
    db = Database(config.DATABASE_URL)
    await db.create_tables()
    
    async with db.async_session() as session:
        # Проверяем, существует ли пользователь с username @terentiev_v
        from sqlalchemy import select
        result = await session.execute(
            select(User).where(User.username == 'terentiev_v')
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Создаем пользователя
            user = User(
                telegram_id=638593776,  # Временное значение, нужно получить реальный ID
                username='terentiev_v',
                language='en',
                created_at=datetime.utcnow()
            )
            session.add(user)
            await session.flush()  # Получаем ID пользователя
            
            print(f"✅ Created user: {user.username} (ID: {user.id})")
        
        # Проверяем подписку
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            # Создаем бесконечную подписку (100 лет)
            subscription = Subscription(
                user_id=user.id,
                is_active=True,
                plan_type='infinite',
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=365*100),  # 100 лет
                payment_method='admin_grant',
                transaction_id=f'admin_grant_{int(datetime.utcnow().timestamp())}'
            )
            session.add(subscription)
            await session.commit()
            print(f"✅ Created infinite subscription for {user.username}")
        else:
            # Обновляем подписку на бесконечную
            subscription.is_active = True
            subscription.plan_type = 'infinite'
            subscription.start_date = datetime.utcnow()
            subscription.end_date = datetime.utcnow() + timedelta(days=365*100)
            subscription.payment_method = 'admin_grant'
            await session.commit()
            print(f"✅ Updated subscription to infinite for {user.username}")

async def get_user_telegram_id():
    """Helper to get Telegram ID for a username"""
    from aiogram import Bot
    bot = Bot(token=config.BOT_TOKEN)
    
    try:
        # Пробуем получить информацию о пользователе
        user = await bot.get_chat('@terentiev_v')
        if user:
            print(f"📱 Telegram user found:")
            print(f"   ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Full name: {user.full_name}")
            return user.id
    except Exception as e:
        print(f"⚠️ Cannot get user info: {e}")
        print("📝 Please provide your Telegram ID manually")
        print("   You can get it from @userinfobot")
        return None

if __name__ == '__main__':
    # Сначала получаем Telegram ID
    telegram_id = asyncio.run(get_user_telegram_id())
    
    if telegram_id:
        # Обновляем конфиг с реальным Telegram ID
        import sys
        sys.path.append('..')
        from bot.database import async_session
        from sqlalchemy import select, update
        
        async def update_telegram_id():
            async with async_session() as session:
                await session.execute(
                    update(User)
                    .where(User.username == 'terentiev_v')
                    .values(telegram_id=telegram_id)
                )
                await session.commit()
                print(f"✅ Updated Telegram ID: {telegram_id}")
        
        asyncio.run(update_telegram_id())
    
    # Инициализируем базу данных
    asyncio.run(init_database())