from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.keyboards.settings_menu import (
    get_settings_main_keyboard,
    get_language_selection_keyboard,
    get_game_settings_keyboard,
    get_specific_game_settings_keyboard,
    get_compare_depth_keyboard,
    get_notification_settings_keyboard,
    get_privacy_settings_keyboard,
    get_auto_update_settings_keyboard,
    get_appearance_settings_keyboard,
    get_security_settings_keyboard,
    get_data_deletion_keyboard,
    get_confirmation_keyboard
)
from bot.utils.localization import get_text
from bot.database import async_session
from sqlalchemy import select, and_
from bot.models.game_account import GameAccount
from bot.models.game_stats import GameSettings

async def settings_command(message: types.Message, state: FSMContext):
    """Команда /settings"""
    await state.finish()
    
    lang = message.from_user.language_code or 'en'
    
    await message.answer(
        "⚙️ <b>Настройки бота</b>\n\nВыберите раздел для настройки:",
        reply_markup=get_settings_main_keyboard(lang),
        parse_mode='HTML'
    )

async def settings_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки настроек"""
    await callback.answer()
    await settings_command(callback.message, state)

async def settings_language(callback: types.CallbackQuery, state: FSMContext):
    """Настройки языка"""
    lang = callback.from_user.language_code or 'en'
    
    await callback.message.edit_text(
        "🌍 <b>Выберите язык интерфейса:</b>",
        reply_markup=get_language_selection_keyboard(lang),
        parse_mode='HTML'
    )

async def set_language(callback: types.CallbackQuery, state: FSMContext):
    """Установка языка"""
    lang_code = callback.data.replace('set_language_', '')
    
    async with async_session() as session:
        from bot.models.user import User
        
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.language = lang_code
            await session.commit()
    
    await callback.answer(f"✅ Язык изменен на {lang_code}")
    await settings_language(callback, state)

async def settings_games(callback: types.CallbackQuery, state: FSMContext):
    """Настройки игр"""
    lang = callback.from_user.language_code or 'en'
    
    await callback.message.edit_text(
        "🎮 <b>Настройки игр:</b>\n\nВыберите игру для настройки:",
        reply_markup=get_game_settings_keyboard(lang),
        parse_mode='HTML'
    )

async def game_settings_specific(callback: types.CallbackQuery, state: FSMContext):
    """Настройки конкретной игры"""
    game = callback.data.replace('game_settings_', '')
    lang = callback.from_user.language_code or 'en'
    
    async with async_session() as session:
        # Получаем настройки игры
        result = await session.execute(
            select(GameSettings).join(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == game
                )
            )
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            # Создаем дефолтные настройки
            settings_data = {
                'auto_update': True,
                'compare_depth': 3,
                'detailed_stats': True,
                'notifications': True
            }
        else:
            settings_data = {
                'auto_update': settings.auto_update,
                'compare_depth': settings.compare_depth,
                'detailed_stats': settings.detailed_stats,
                'notifications': settings.notifications
            }
    
    game_names = {
        'csgo': 'CS:GO',
        'dota2': 'Dota 2',
        'valorant': 'Valorant',
        'lol': 'League of Legends',
        'wot': 'World of Tanks',
        'pubg': 'PUBG'
    }
    
    game_name = game_names.get(game, game)
    
    await callback.message.edit_text(
        f"🎮 <b>Настройки {game_name}:</b>",
        reply_markup=get_specific_game_settings_keyboard(lang, game, settings_data),
        parse_mode='HTML'
    )

async def toggle_auto_update(callback: types.CallbackQuery, state: FSMContext):
    """Включить/выключить автообновление для игры"""
    data = callback.data.replace('toggle_auto_update_', '')
    game = data
    
    async with async_session() as session:
        result = await session.execute(
            select(GameSettings).join(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == game
                )
            )
        )
        settings = result.scalar_one_or_none()
        
        if settings:
            settings.auto_update = not settings.auto_update
            await session.commit()
            await callback.answer(f"✅ Автообновление {'включено' if settings.auto_update else 'выключено'}")
        else:
            await callback.answer("❌ Настройки игры не найдены")
    
    await game_settings_specific(callback, state)

async def set_compare_depth(callback: types.CallbackQuery, state: FSMContext):
    """Установить глубину сравнения"""
    game = callback.data.replace('set_compare_depth_', '')
    lang = callback.from_user.language_code or 'en'
    
    async with async_session() as session:
        result = await session.execute(
            select(GameSettings).join(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == game
                )
            )
        )
        settings = result.scalar_one_or_none()
        
        current_depth = settings.compare_depth if settings else 3
    
    await callback.message.edit_text(
        "📊 <b>Выберите глубину сравнения:</b>\n\n"
        "Сколько последних игр использовать для сравнения статистики?",
        reply_markup=get_compare_depth_keyboard(lang, game, current_depth),
        parse_mode='HTML'
    )

async def set_depth_value(callback: types.CallbackQuery, state: FSMContext):
    """Установить значение глубины"""
    data = callback.data.replace('set_depth_', '')
    game, depth_str = data.split('_')
    depth = int(depth_str)
    
    async with async_session() as session:
        result = await session.execute(
            select(GameSettings).join(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == game
                )
            )
        )
        settings = result.scalar_one_or_none()
        
        if settings:
            settings.compare_depth = depth
            await session.commit()
            await callback.answer(f"✅ Глубина сравнения установлена: {depth} игр")
        else:
            await callback.answer("❌ Настройки игры не найдены")
    
    await game_settings_specific(callback, state)

def register_settings_handlers(dp: Dispatcher):
    """Регистрация обработчиков настроек"""
    dp.register_message_handler(settings_command, Command('settings'), state="*")
    dp.register_message_handler(settings_command, lambda m: m.text in ['⚙️ Настройки', '⚙️ Settings'], state="*")
    
    dp.register_callback_query_handler(settings_callback, lambda c: c.data == 'settings', state="*")
    dp.register_callback_query_handler(settings_language, lambda c: c.data == 'settings_language')
    dp.register_callback_query_handler(set_language, lambda c: c.data.startswith('set_language_'))
    dp.register_callback_query_handler(settings_games, lambda c: c.data == 'settings_games')
    dp.register_callback_query_handler(game_settings_specific, lambda c: c.data.startswith('game_settings_'))
    dp.register_callback_query_handler(toggle_auto_update, lambda c: c.data.startswith('toggle_auto_update_'))
    dp.register_callback_query_handler(set_compare_depth, lambda c: c.data.startswith('set_compare_depth_'))
    dp.register_callback_query_handler(set_depth_value, lambda c: c.data.startswith('set_depth_'))