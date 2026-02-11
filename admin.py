from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from bot.config import config
from bot.database import async_session
from sqlalchemy import select, update, delete
from bot.models.user import User
from bot.models.subscription import Subscription
from datetime import datetime, timedelta

async def admin_panel(message: types.Message):
    """Admin panel command"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
        types.InlineKeyboardButton("💎 Подписки", callback_data="admin_subs"),
        types.InlineKeyboardButton("⚙️ Настройки", callback_data="admin_settings")
    )
    
    await message.answer("🔧 Панель администратора:", reply_markup=keyboard)

async def admin_statistics(callback: types.CallbackQuery):
    """Show bot statistics"""
    async with async_session() as session:
        # Total users
        result = await session.execute(select(User))
        total_users = len(result.scalars().all())
        
        # Active subscriptions
        result = await session.execute(
            select(Subscription).where(Subscription.is_active == True)
        )
        active_subs = len(result.scalars().all())
        
        # Today's matches
        result = await session.execute(
            select(Match).where(Match.start_time >= datetime.utcnow().date())
        )
        today_matches = len(result.scalars().all())
    
    stats_text = f"""
📊 <b>Статистика бота:</b>

👥 Всего пользователей: {total_users}
💎 Активных подписок: {active_subs}
🎮 Матчей сегодня: {today_matches}
📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """
    
    await callback.message.edit_text(stats_text, parse_mode='HTML')

async def manage_subscription(callback: types.CallbackQuery):
    """Manage user subscription"""
    data = callback.data.split(':')
    user_id = int(data[1])
    action = data[2]
    
    async with async_session() as session:
        if action == 'activate':
            # Activate subscription for 30 days
            end_date = datetime.utcnow() + timedelta(days=30)
            await session.execute(
                update(Subscription)
                .where(Subscription.user_id == user_id)
                .values(is_active=True, end_date=end_date)
            )
            await session.commit()
            await callback.answer("✅ Подписка активирована")
        elif action == 'deactivate':
            await session.execute(
                update(Subscription)
                .where(Subscription.user_id == user_id)
                .values(is_active=False)
            )
            await session.commit()
            await callback.answer("❌ Подписка деактивирована")
        elif action == 'extend':
            # Extend by 30 days
            await session.execute(
                update(Subscription)
                .where(Subscription.user_id == user_id)
                .values(end_date=Subscription.end_date + timedelta(days=30))
            )
            await session.commit()
            await callback.answer("📅 Подписка продлена")

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, Command('admin'))
    dp.register_callback_query_handler(admin_statistics, lambda c: c.data == 'admin_stats')
    # Add more admin handlers as needed