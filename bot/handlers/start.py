from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from bot.keyboards.main_menu import get_main_menu
from bot.utils.localization import get_text
from bot.database import async_session
from sqlalchemy import select
from bot.models.user import User

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    
    async with async_session() as session:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                language=message.from_user.language_code or 'en'
            )
            session.add(user)
            await session.commit()
        
        # Get localized welcome text
        welcome_text = get_text('welcome_message', user.language)
        example_text = get_text('example_statistics', user.language)
        
        full_text = f"{welcome_text}\n\n{example_text}"
        
        await message.answer(
            full_text,
            reply_markup=get_main_menu(user.language),
            parse_mode='HTML'
        )

async def cmd_help(message: types.Message):
    lang = message.from_user.language_code or 'en'
    help_text = get_text('help_message', lang)
    
    await message.answer(help_text, parse_mode='HTML')

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, CommandStart(), state="*")
    dp.register_message_handler(cmd_help, commands=['help'])