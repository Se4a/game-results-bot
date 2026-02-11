from aiogram import Bot
from datetime import datetime, timedelta
from bot.utils.localization import get_text
from bot.database import async_session
from sqlalchemy import select, and_

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.message_counters = {}  # Счетчик сообщений для партнерских интеграций
    
    async def send_match_start_notification(self, user_id: int, language: str, game: str):
        """Отправить уведомление о начале матча"""
        text = get_text('notifications.match_started', language).format(game=game.upper())
        await self.bot.send_message(user_id, text)
        
        # Увеличиваем счетчик сообщений
        self.message_counters[user_id] = self.message_counters.get(user_id, 0) + 1
        
        # Каждое 5-е сообщение отправляем благодарность
        if self.message_counters.get(user_id, 0) % 5 == 0:
            await self.send_thank_you_message(user_id, language)
    
    async def send_thank_you_message(self, user_id: int, language: str):
        """Отправить благодарственное сообщение"""
        text = get_text('notifications.thank_you', language)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            get_text('buttons.support', language),
            url='https://t.me/terentiev_v'
        ))
        
        await self.bot.send_message(user_id, text, reply_markup=keyboard)
    
    async def send_daily_limit_reached(self, user_id: int, language: str):
        """Уведомление о достижении дневного лимита"""
        text = get_text('notifications.daily_limit', language)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            get_text('menu.subscription', language),
            callback_data='subscription_menu'
        ))
        
        await self.bot.send_message(user_id, text, reply_markup=keyboard)
    
    async def send_subscription_reminder(self, user_id: int, language: str, days_left: int):
        """Напоминание об истечении подписки"""
        text = get_text('notifications.subscription_expiring', language).format(days=days_left)
        
        keyboard = InlineKeyboardMarkup()
        if days_left <= 1:
            keyboard.add(InlineKeyboardButton(
                get_text('buttons.renew', language),
                callback_data='subscription_menu'
            ))
        
        await self.bot.send_message(user_id, text, reply_markup=keyboard)
    
    async def send_match_report(self, user_id: int, language: str, match_data: dict):
        """Отправить отчет о матче"""
        # Форматируем статистику в таблицу
        table = self.format_match_table(match_data)
        
        text = f"""
🎮 <b>{match_data['game'].upper()} | ОТЧЕТ О МАТЧЕ</b>
👤 Аккаунт: {match_data['player_name']}
🏆 Результат: {match_data['result']}
📅 Дата: {match_data['date']}
⏱️ Время: {match_data['duration']}

<b>Статистика:</b>
{table}

📊 Ваш средний KDA: {match_data.get('avg_kda', 'N/A')}
🎯 Ваш средний ADR: {match_data.get('avg_adr', 'N/A')}
"""
        
        await self.bot.send_message(user_id, text, parse_mode='HTML')
    
    def format_match_table(self, match_data: dict) -> str:
        """Форматировать таблицу статистики"""
        players = match_data.get('players', [])
        
        if not players:
            return "Нет данных об игроках"
        
        # Формируем таблицу
        header = "<code>Игрок           | K  | A  | D  | K/D  | ADR\n"
        separator = "-" * 50 + "\n"
        
        rows = []
        for player in players:
            row = f"{player['name'][:15]:<15} | "
            row += f"{player.get('kills', 0):<2} | "
            row += f"{player.get('assists', 0):<2} | "
            row += f"{player.get('deaths', 0):<2} | "
            row += f"{player.get('kd', 0):<4.1f} | "
            row += f"{player.get('adr', 0):<4}"
            rows.append(row)
        
        return header + separator + "\n".join(rows) + "</code>"
    
    async def send_admin_notification(self, message: str):
        """Отправить уведомление администратору"""
        from bot.config import config
        
        for admin_id in config.ADMIN_IDS:
            try:
                await self.bot.send_message(admin_id, f"👨‍💼 АДМИН: {message}")
            except Exception as e:
                print(f"Error sending admin notification: {e}")