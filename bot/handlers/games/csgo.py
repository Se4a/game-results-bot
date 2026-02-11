from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.keyboards.games_menu import get_csgo_menu
from bot.utils.localization import get_text
from bot.services.api_client import SteamAPIClient
from bot.database import async_session
from sqlalchemy import select, and_
from datetime import datetime
import asyncio

class CSGOStates(StatesGroup):
    waiting_for_steam_id = State()
    waiting_for_confirm = State()

async def csgo_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    
    lang = callback.from_user.language_code or 'en'
    guide_text = get_text('guides.csgo', lang)
    
    await callback.message.edit_text(
        guide_text,
        reply_markup=get_csgo_menu(lang),
        parse_mode='HTML'
    )

async def bind_steam_account(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.from_user.language_code or 'en'
    await CSGOStates.waiting_for_steam_id.set()
    
    guide = "To find your Steam ID:\n1. Open Steam client\n2. Click on your profile name\n3. Click 'View profile'\n4. The URL will contain your Steam ID\n\nExample: https://steamcommunity.com/profiles/76561198012345678/\nSteam ID: 76561198012345678\n\nPlease enter your Steam ID:"
    
    await callback.message.edit_text(guide)

async def process_steam_id(message: types.Message, state: FSMContext):
    steam_id = message.text.strip()
    lang = message.from_user.language_code or 'en'
    
    # Validate Steam ID
    if not steam_id.isdigit() or len(steam_id) != 17:
        await message.answer(get_text('errors.invalid_steam_id', lang))
        return
    
    # Check cooldown for account change
    async with async_session() as session:
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == message.from_user.id,
                    GameAccount.game == 'csgo'
                )
            )
        )
        existing_account = result.scalar_one_or_none()
        
        if existing_account:
            # Check if 48 hours have passed
            time_diff = datetime.utcnow() - existing_account.last_changed
            if time_diff.total_seconds() < 48 * 3600:
                hours_left = 48 - (time_diff.total_seconds() / 3600)
                await message.answer(
                    get_text('errors.account_change_cooldown', lang).format(hours=round(hours_left, 1))
                )
                return
    
    # Verify Steam account
    api_client = SteamAPIClient()
    is_valid = await api_client.verify_steam_account(steam_id)
    
    if not is_valid:
        await message.answer(get_text('errors.invalid_account', lang))
        return
    
    await state.update_data(steam_id=steam_id)
    await CSGOStates.waiting_for_confirm.set()
    
    confirm_text = get_text('confirm_account_binding', lang).format(
        game='CS:GO',
        id=steam_id
    )
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            get_text('yes', lang),
            callback_data='confirm_bind'
        ),
        InlineKeyboardButton(
            get_text('no', lang),
            callback_data='cancel_bind'
        )
    )
    
    await message.answer(confirm_text, reply_markup=keyboard)

async def confirm_binding(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.from_user.language_code or 'en'
    data = await state.get_data()
    steam_id = data.get('steam_id')
    
    async with async_session() as session:
        # Remove old account if exists
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == callback.from_user.id,
                    GameAccount.game == 'csgo'
                )
            )
        )
        old_account = result.scalar_one_or_none()
        
        if old_account:
            await session.delete(old_account)
        
        # Create new account
        new_account = GameAccount(
            user_id=callback.from_user.id,
            game='csgo',
            account_id=steam_id,
            nickname=f"Steam_{steam_id[-8:]}",
            last_changed=datetime.utcnow(),
            is_verified=True
        )
        session.add(new_account)
        
        # Create default settings
        settings = GameSettings(
            game_account_id=new_account.id,
            compare_depth=3,
            auto_update=True,
            notifications=True
        )
        session.add(settings)
        
        await session.commit()
    
    await state.finish()
    
    # Get recent matches
    await get_recent_matches(callback.from_user.id, lang, callback.message)
    
    success_text = get_text('account_bound_success', lang).format(game='CS:GO')
    await callback.message.edit_text(success_text)

async def get_recent_matches(user_id: int, lang: str, message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(GameAccount).where(
                and_(
                    GameAccount.user_id == user_id,
                    GameAccount.game == 'csgo'
                )
            )
        )
        account = result.scalar_one_or_none()
        
        if not account:
            return
        
        # Fetch matches from Steam API
        api_client = SteamAPIClient()
        matches = await api_client.get_csgo_matches(account.account_id, limit=3)
        
        if matches:
            # Process and display matches
            for match in matches:
                stats_text = format_match_stats(match, lang)
                await message.answer(stats_text, parse_mode='HTML')
        else:
            no_matches_text = get_text('no_recent_matches', lang)
            await message.answer(no_matches_text)

def format_match_stats(match_data: dict, lang: str) -> str:
    """Format match statistics into a table"""
    table = f"""
🎮 <b>CS:GO | MATCH REPORT</b>
👤 Account: {match_data.get('player_name', 'Unknown')}
🏆 Result: {match_data.get('result', 'Unknown')}
📅 Date: {match_data.get('date', 'N/A')}
⏱️ Time: {match_data.get('duration', 'N/A')}

<b>Statistics:</b>
<code>
Player          | K  | A  | D  | K/D | ADR  | HS%   | MVP
{'-'*50}
{match_data.get('player_stats', {}).get('name', 'Player'):<15} | {match_data.get('player_stats', {}).get('kills', 0):<2} | {match_data.get('player_stats', {}).get('assists', 0):<2} | {match_data.get('player_stats', {}).get('deaths', 0):<2} | {match_data.get('player_stats', {}).get('kd', 0):<3.1f} | {match_data.get('player_stats', {}).get('adr', 0):<4} | {match_data.get('player_stats', {}).get('hs_percent', 0):<4.1f} | {match_data.get('player_stats', {}).get('mvp', 0)}
</code>

📊 Your AVG KDA: {match_data.get('avg_kda', 'N/A')}
🎯 Your AVG ADR: {match_data.get('avg_adr', 'N/A')}
"""
    return table

def register_csgo_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(csgo_menu, lambda c: c.data == 'game_csgo')
    dp.register_callback_query_handler(bind_steam_account, lambda c: c.data == 'bind_csgo')
    dp.register_message_handler(process_steam_id, state=CSGOStates.waiting_for_steam_id)
    dp.register_callback_query_handler(confirm_binding, lambda c: c.data == 'confirm_bind', state=CSGOStates.waiting_for_confirm)
    dp.register_callback_query_handler(csgo_menu, lambda c: c.data == 'cancel_bind', state='*')