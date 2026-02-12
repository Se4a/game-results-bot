from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.games_menu import get_game_detailed_menu
from bot.utils.localization import get_text
from bot.services.api_client import SteamAPIClient
from bot.database import async_session
from sqlalchemy import select, and_
from datetime import datetime

class DotaStates(StatesGroup):
    waiting_for_steam_id = State()
    waiting_for_confirm = State()

async def dota_menu(callback: types.CallbackQuery, state: FSMContext):
    """Меню Dota 2"""
    await state.finish()
    lang = callback.from_user.language_code or 'en'
    
    guide_text = get_text('guides.dota', lang)
    await callback.message.edit_text(
        guide_text,
        reply_markup=get_game_detailed_menu('dota2', lang),
        parse_mode='HTML'
    )

async def bind_dota_account(callback: types.CallbackQuery, state: FSMContext):
    """Привязка Steam аккаунта для Dota 2"""
    lang = callback.from_user.language_code or 'en'
    await DotaStates.waiting_for_steam_id.set()
    
    guide = get_text('guides.dota_bind', lang)
    await callback.message.edit_text(guide)

async def process_steam_id(message: types.Message, state: FSMContext):
    """Обработка введённого Steam ID"""
    steam_id = message.text.strip()
    lang = message.from_user.language_code or 'en'
    
    # Валидация Steam ID
    if not steam_id.isdigit() or len(steam_id) != 17:
        await message.answer(get_text('errors.invalid_steam_id', lang))
        return
    
    # Проверка cooldown смены аккаунта
    async with async_session() as session:
        from bot.models.game_account import GameAccount
        from bot.models.game_stats import GameSettings
        
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == message.from_user.id,
                    GameAccount.game == 'dota2'
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing and not existing.can_be_changed:
            hours = existing.hours_until_change
            await message.answer(
                get_text('errors.account_change_cooldown', lang).format(hours=hours)
            )
            return
    
    # Проверка аккаунта через Steam API
    api_client = SteamAPIClient()
    is_valid = await api_client.verify_steam_account(steam_id)
    
    if not is_valid:
        await message.answer(get_text('errors.invalid_account', lang))
        return
    
    await state.update_data(steam_id=steam_id)
    await DotaStates.waiting_for_confirm.set()
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(get_text('yes', lang), callback_data='confirm_dota_bind'),
        InlineKeyboardButton(get_text('no', lang), callback_data='cancel_dota_bind')
    )
    
    confirm_text = get_text('confirm_account_binding', lang).format(
        game='Dota 2',
        id=steam_id
    )
    await message.answer(confirm_text, reply_markup=keyboard)

async def confirm_binding(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение привязки аккаунта"""
    lang = callback.from_user.language_code or 'en'
    data = await state.get_data()
    steam_id = data.get('steam_id')
    
    async with async_session() as session:
        from bot.models.game_account import GameAccount
        from bot.models.game_stats import GameSettings
        from bot.models.user import User
        
        # Удаляем старый аккаунт, если есть
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == 'dota2'
                )
            )
        )
        old = result.scalar_one_or_none()
        if old:
            await session.delete(old)
        
        # Создаём новый
        user_result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_result.scalar_one()
        
        new_account = GameAccount(
            user_id=user.id,
            game='dota2',
            account_id=steam_id,
            nickname=f"Steam_{steam_id[-8:]}",
            region='global',
            last_changed=datetime.utcnow(),
            is_verified=True
        )
        session.add(new_account)
        await session.flush()
        
        # Создаём настройки
        settings = GameSettings(
            game_account_id=new_account.id,
            compare_depth=3,
            auto_update=True,
            notifications=True,
            detailed_stats=True
        )
        session.add(settings)
        await session.commit()
    
    await state.finish()
    await callback.message.edit_text(
        get_text('account_bound_success', lang).format(game='Dota 2')
    )

def register_dota_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(dota_menu, lambda c: c.data == 'game_dota')
    dp.register_callback_query_handler(bind_dota_account, lambda c: c.data == 'bind_dota')
    dp.register_message_handler(process_steam_id, state=DotaStates.waiting_for_steam_id)
    dp.register_callback_query_handler(confirm_binding, lambda c: c.data == 'confirm_dota_bind', state=DotaStates.waiting_for_confirm)
    dp.register_callback_query_handler(dota_menu, lambda c: c.data == 'cancel_dota_bind', state='*')