from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.keyboards.main_menu import get_subscription_menu
from bot.utils.localization import get_text
from bot.database import async_session
from sqlalchemy import select, and_
from datetime import datetime

async def subscription_menu(message: types.Message, state: FSMContext):
    """Меню подписки"""
    await state.finish()
    
    lang = message.from_user.language_code or 'en'
    
    async with async_session() as session:
        from bot.database import Subscription
        
        # Получаем информацию о подписке пользователя
        result = await session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == message.from_user.id,
                    Subscription.is_active == True
                )
            )
        )
        subscription = result.scalar_one_or_none()
    
    if subscription and subscription.end_date > datetime.now():
        # Пользователь имеет активную подписку
        text = get_text('subscription.active', lang).format(
            date=subscription.end_date.strftime('%d.%m.%Y')
        )
        
        # Добавляем информацию о типе подписки
        plan_names = {
            '1_month': '1 месяц',
            '3_months': '3 месяца',
            '6_months': '6 месяцев',
            '12_months': '12 месяцев',
            'infinite': 'Бесконечная подписка'
        }
        
        plan_name = plan_names.get(subscription.plan_type, subscription.plan_type)
        text += f"\n📅 План: {plan_name}"
        text += f"\n💰 Способ оплаты: {subscription.payment_method}"
        text += f"\n📊 Дней осталось: {(subscription.end_date - datetime.now()).days}"
        
        has_active_sub = True
    else:
        # Нет активной подписки
        text = get_text('subscription.inactive', lang)
        text += "\n\n💎 <b>Доступные планы:</b>"
        text += "\n• 1 месяц - $0.99 / 99 ⭐"
        text += "\n• 3 месяца - $2.50 / 250 ⭐ (экономия 16%)"
        text += "\n• 6 месяцев - $5.00 / 500 ⭐ (экономия 16%)"
        text += "\n• 12 месяцев - $10.00 / 1000 ⭐ (экономия 16%)"
        text += "\n\n⭐ <b>Telegram Stars</b> - внутренняя валюта Telegram для оплаты в ботах"
        text += "\n💱 Курс: 1 Star = $0.01"
        
        has_active_sub = False
    
    await message.answer(
        text,
        reply_markup=get_subscription_menu(lang, has_active_sub),
        parse_mode='HTML'
    )

async def subscription_command(message: types.Message, state: FSMContext):
    """Команда /subscription"""
    await subscription_menu(message, state)

async def back_to_subscription(callback: types.CallbackQuery, state: FSMContext):
    """Возврат в меню подписки"""
    await state.finish()
    lang = callback.from_user.language_code or 'en'
    
    async with async_session() as session:
        from bot.database import Subscription
        
        result = await session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == callback.from_user.id,
                    Subscription.is_active == True
                )
            )
        )
        subscription = result.scalar_one_or_none()
    
    has_active_sub = bool(subscription and subscription.end_date > datetime.now())
    
    await callback.message.edit_text(
        get_text('subscription.choose_plan', lang),
        reply_markup=get_subscription_menu(lang, has_active_sub)
    )

def register_subscription_handlers(dp: Dispatcher):
    dp.register_message_handler(subscription_command, Command('subscription', 'sub'), state="*")
    dp.register_message_handler(subscription_menu, lambda m: m.text in ['💎 Подписка', '💎 Subscription'], state="*")
    dp.register_callback_query_handler(back_to_subscription, lambda c: c.data == 'back_to_subscription', state="*")