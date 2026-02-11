from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.config import config
from bot.database import async_session
from sqlalchemy import select, update, delete
from datetime import datetime, timedelta
import re

class AdminStates(StatesGroup):
    managing_user = State()
    setting_subscription = State()
    adding_match = State()

async def admin_command(message: types.Message):
    """Админ-панель"""
    if message.from_user.id not in config.ADMIN_IDS:
        await message.answer("⛔ Доступ запрещен")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("👤 Управление пользователями", callback_data="admin_users"),
        types.InlineKeyboardButton("💎 Управление подписками", callback_data="admin_subs"),
        types.InlineKeyboardButton("🎮 Добавить матч", callback_data="admin_add_match"),
        types.InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")
    )
    
    await message.answer("🔧 Панель администратора:", reply_markup=keyboard)

async def admin_users_menu(callback: types.CallbackQuery):
    """Меню управления пользователями"""
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("🔍 Найти пользователя", callback_data="admin_find_user"),
        types.InlineKeyboardButton("📋 Список пользователей", callback_data="admin_list_users"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="admin_back")
    )
    
    await callback.message.edit_text("👤 Управление пользователями:", reply_markup=keyboard)

async def admin_find_user(callback: types.CallbackQuery, state: FSMContext):
    """Поиск пользователя"""
    await callback.message.edit_text("Введите Telegram ID или username пользователя (@username):")
    await AdminStates.managing_user.set()

async def admin_process_user_search(message: types.Message, state: FSMContext):
    """Обработка поиска пользователя"""
    search_query = message.text.strip()
    
    async with async_session() as session:
        # Пробуем найти по Telegram ID
        if search_query.isdigit():
            result = await session.execute(
                select(User).where(User.telegram_id == int(search_query))
            )
            user = result.scalar_one_or_none()
        # Ищем по username
        elif search_query.startswith('@'):
            result = await session.execute(
                select(User).where(User.username == search_query[1:])
            )
            user = result.scalar_one_or_none()
        else:
            # Ищем по части username
            result = await session.execute(
                select(User).where(User.username.contains(search_query))
            )
            users = result.scalars().all()
            
            if len(users) == 1:
                user = users[0]
            elif len(users) > 1:
                text = "Найдено несколько пользователей:\n\n"
                for u in users[:10]:  # Ограничим 10 пользователями
                    text += f"👤 {u.username} (ID: {u.telegram_id})\n"
                
                await message.answer(text)
                return
            else:
                await message.answer("Пользователь не найден")
                return
    
    if not user:
        await message.answer("Пользователь не найден")
        return
    
    # Показываем информацию о пользователе
    async with async_session() as session:
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        subscription = result.scalar_one_or_none()
    
    text = f"👤 <b>Информация о пользователе:</b>\n\n"
    text += f"ID: {user.id}\n"
    text += f"Telegram ID: {user.telegram_id}\n"
    text += f"Username: @{user.username}\n"
    text += f"Язык: {user.language}\n"
    text += f"Дата регистрации: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    if subscription:
        text += f"💎 <b>Подписка:</b>\n"
        text += f"Тип: {subscription.plan_type}\n"
        text += f"Активна: {'✅ Да' if subscription.is_active else '❌ Нет'}\n"
        text += f"Начало: {subscription.start_date.strftime('%d.%m.%Y')}\n"
        text += f"Окончание: {subscription.end_date.strftime('%d.%m.%Y')}\n"
        text += f"Способ оплаты: {subscription.payment_method}\n"
    else:
        text += "❌ Нет подписки\n"
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("💎 Управление подпиской", callback_data=f"admin_sub_{user.id}"),
        types.InlineKeyboardButton("🎮 Аккаунты игр", callback_data=f"admin_games_{user.id}"),
        types.InlineKeyboardButton("📊 Статистика", callback_data=f"admin_user_stats_{user.id}"),
        types.InlineKeyboardButton("🚫 Блокировка", callback_data=f"admin_ban_{user.id}")
    )
    
    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)
    await state.finish()

async def admin_manage_subscription(callback: types.CallbackQuery):
    """Управление подпиской пользователя"""
    user_id = int(callback.data.split('_')[2])
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("♾️ Бесконечная подписка", callback_data=f"admin_sub_infinite_{user_id}"),
        types.InlineKeyboardButton("📅 1 месяц", callback_data=f"admin_sub_1month_{user_id}"),
        types.InlineKeyboardButton("📅 3 месяца", callback_data=f"admin_sub_3months_{user_id}"),
        types.InlineKeyboardButton("📅 6 месяцев", callback_data=f"admin_sub_6months_{user_id}"),
        types.InlineKeyboardButton("📅 12 месяцев", callback_data=f"admin_sub_12months_{user_id}"),
        types.InlineKeyboardButton("❌ Отменить подписку", callback_data=f"admin_sub_cancel_{user_id}"),
        types.InlineKeyboardButton("🔙 Назад", callback_data=f"admin_back_to_user_{user_id}")
    )
    
    await callback.message.edit_text("Выберите действие с подпиской:", reply_markup=keyboard)

async def admin_set_subscription(callback: types.CallbackQuery):
    """Установка подписки"""
    data = callback.data.split('_')
    action = data[2]
    target_user_id = int(data[3])
    
    async with async_session() as session:
        # Находим пользователя
        result = await session.execute(
            select(User).where(User.id == target_user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await callback.answer("Пользователь не найден")
            return
        
        # Находим подписку
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        subscription = result.scalar_one_or_none()
        
        now = datetime.utcnow()
        
        if action == 'cancel':
            # Отменяем подписку
            if subscription:
                subscription.is_active = False
                await session.commit()
                await callback.answer("✅ Подписка отменена")
        elif action == 'infinite':
            # Бесконечная подписка (100 лет)
            end_date = now + timedelta(days=365*100)
            
            if subscription:
                subscription.is_active = True
                subscription.plan_type = 'infinite'
                subscription.start_date = now
                subscription.end_date = end_date
                subscription.payment_method = 'admin'
            else:
                subscription = Subscription(
                    user_id=user.id,
                    is_active=True,
                    plan_type='infinite',
                    start_date=now,
                    end_date=end_date,
                    payment_method='admin',
                    transaction_id=f'admin_{int(now.timestamp())}'
                )
                session.add(subscription)
            
            await session.commit()
            await callback.answer("✅ Бесконечная подписка установлена")
        else:
            # Временная подписка
            months = int(action.replace('month', '').replace('s', ''))
            end_date = now + timedelta(days=30 * months)
            
            if subscription:
                subscription.is_active = True
                subscription.plan_type = f'{months}_months'
                subscription.start_date = now
                subscription.end_date = end_date
                subscription.payment_method = 'admin'
            else:
                subscription = Subscription(
                    user_id=user.id,
                    is_active=True,
                    plan_type=f'{months}_months',
                    start_date=now,
                    end_date=end_date,
                    payment_method='admin',
                    transaction_id=f'admin_{int(now.timestamp())}'
                )
                session.add(subscription)
            
            await session.commit()
            await callback.answer(f"✅ Подписка на {months} месяцев установлена")
    
    # Возвращаемся к информации о пользователе
    await admin_process_user_search(callback.message, None)

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_command, Command('admin'))
    dp.register_callback_query_handler(admin_users_menu, lambda c: c.data == 'admin_users')
    dp.register_callback_query_handler(admin_find_user, lambda c: c.data == 'admin_find_user')
    dp.register_message_handler(admin_process_user_search, state=AdminStates.managing_user)
    dp.register_callback_query_handler(admin_manage_subscription, lambda c: c.data.startswith('admin_sub_') and len(c.data.split('_')) == 3)
    dp.register_callback_query_handler(admin_set_subscription, lambda c: c.data.startswith('admin_sub_') and len(c.data.split('_')) == 4)