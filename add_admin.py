#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.database import async_session
from sqlalchemy import select, update
from aiogram import Bot
from bot.config import config

async def add_admin(username: str):
    """Добавить пользователя как администратора"""
    # Получаем Telegram ID по username
    bot = Bot(token=config.BOT_TOKEN)
    
    try:
        user = await bot.get_chat(username)
        telegram_id = user.id
        
        print(f"✅ Найден пользователь:")
        print(f"   ID: {telegram_id}")
        print(f"   Username: {user.username}")
        print(f"   Full name: {user.full_name}")
        
        # Добавляем ID в список администраторов
        current_admins = config.ADMIN_IDS.copy()
        if telegram_id not in current_admins:
            current_admins.append(telegram_id)
            
            # Обновляем переменную окружения (в реальности нужно обновить .env файл)
            print(f"\n📝 Добавьте следующий ID в переменную окружения ADMIN_IDS:")
            print(f"   ADMIN_IDS={','.join(map(str, current_admins))}")
            
            # Обновляем запись в базе данных (если нужно)
            async with async_session() as session:
                result = await session.execute(
                    select(User).where(User.telegram_id == telegram_id)
                )
                user_db = result.scalar_one_or_none()
                
                if user_db:
                    print(f"\n✅ Пользователь уже есть в базе данных")
                else:
                    print(f"\n⚠️ Пользователь не найден в базе данных")
                    print("   Он появится после первого запуска команды /start")
        
        else:
            print(f"\nℹ️ Пользователь уже является администратором")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print(f"\n📝 Введите Telegram ID вручную:")
        telegram_id = input("Telegram ID: ").strip()
        
        if telegram_id.isdigit():
            telegram_id = int(telegram_id)
            current_admins = config.ADMIN_IDS.copy()
            if telegram_id not in current_admins:
                current_admins.append(telegram_id)
                print(f"\n📝 Добавьте следующий ID в переменную окружения ADMIN_IDS:")
                print(f"   ADMIN_IDS={','.join(map(str, current_admins))}")
            else:
                print(f"\nℹ️ Пользователь уже является администратором")
        else:
            print("❌ Неверный Telegram ID")
    
    await bot.session.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        if not username.startswith('@'):
            username = '@' + username
        asyncio.run(add_admin(username))
    else:
        print("Использование: python add_admin.py @username")
        print("Пример: python add_admin.py @terentiev_v")