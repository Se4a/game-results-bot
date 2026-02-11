from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.extended_formatters import ExtendedGameFormatter
from bot.services.extended_stats_collector import ExtendedStatsCollector
from bot.database import async_session
from sqlalchemy import select
import asyncio

async def send_complete_stats(callback: types.CallbackQuery, state: FSMContext):
    """Отправить полную статистику игры"""
    
    game = callback.data.replace('complete_stats_', '')
    user_id = callback.from_user.id
    lang = callback.from_user.language_code or 'en'
    
    async with async_session() as session:
        # Получаем привязанный аккаунт
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == user_id,
                    GameAccount.game == game
                )
            )
        )
        account = result.scalar_one_or_none()
        
        if not account:
            await callback.answer("Сначала привяжите аккаунт!")
            return
    
    # Получаем полную статистику
    collector = ExtendedStatsCollector()
    complete_stats = await collector.get_complete_live_stats(
        game, account.account_id, account.region
    )
    
    if not complete_stats:
        await callback.answer("Не удалось получить статистику")
        return
    
    # Форматируем полный отчет
    formatter = ExtendedGameFormatter()
    
    if game == 'csgo':
        report = formatter.format_complete_csgo_report(
            complete_stats, 
            complete_stats.get('player_stats', {}),
            lang
        )
    elif game == 'dota2':
        report = formatter.format_complete_dota_report(
            complete_stats,
            complete_stats.get('player_stats', {}),
            lang
        )
    elif game == 'valorant':
        report = formatter.format_complete_valorant_report(
            complete_stats,
            complete_stats.get('player_stats', {}),
            lang
        )
    elif game == 'lol':
        report = formatter.format_complete_lol_report(
            complete_stats,
            complete_stats.get('player_stats', {}),
            lang
        )
    elif game == 'wot':
        report = formatter.format_complete_wot_report(
            complete_stats,
            complete_stats.get('player_stats', {}),
            lang
        )
    elif game == 'pubg':
        report = formatter.format_complete_pubg_report(
            complete_stats,
            complete_stats.get('player_stats', {}),
            lang
        )
    else:
        report = "Игра не поддерживается"
    
    # Отправляем отчет
    await callback.message.answer(report, parse_mode='HTML')
    
    # Закрываем коллектор
    await collector.close()
    
    await callback.answer()

async def start_live_tracking(callback: types.CallbackQuery, state: FSMContext):
    """Начать live-отслеживание матча"""
    
    game = callback.data.replace('live_track_', '')
    user_id = callback.from_user.id
    
    async with async_session() as session:
        # Получаем привязанный аккаунт
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == user_id,
                    GameAccount.game == game
                )
            )
        )
        account = result.scalar_one_or_none()
        
        if not account:
            await callback.answer("Сначала привяжите аккаунт!")
            return
        
        # Получаем текущий матч (в реальности нужно определять через API)
        current_match_id = f"{game}_{account.account_id}_{int(datetime.now().timestamp())}"
        
        # Начинаем отслеживание
        live_updater = callback.bot.get('live_updater')
        if live_updater:
            await live_updater.start_tracking(
                user_id, game, current_match_id, account.account_id, account.region
            )
            await callback.answer("✅ Live-отслеживание начато!")
        else:
            await callback.answer("❌ Ошибка системы отслеживания")

def register_complete_stats_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(send_complete_stats, lambda c: c.data.startswith('complete_stats_'))
    dp.register_callback_query_handler(start_live_tracking, lambda c: c.data.startswith('live_track_'))