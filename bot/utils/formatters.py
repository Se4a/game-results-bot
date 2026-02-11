from typing import Dict, List, Any
from datetime import datetime, timedelta
from bot.config import config
import json

class GameFormatter:
    """Базовые форматтеры для игровой статистики"""
    
    @staticmethod
    def format_number(value: Any) -> str:
        """Форматирование чисел"""
        if isinstance(value, (int, float)):
            if value >= 1000000:
                return f"{value/1000000:.1f}M"
            elif value >= 1000:
                return f"{value/1000:.1f}K"
            elif isinstance(value, float):
                return f"{value:.2f}"
            else:
                return str(value)
        return str(value)
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Форматирование процентов"""
        return f"{value:.1f}%"
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """Форматирование времени"""
        if seconds < 60:
            return f"{seconds} сек"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02d} мин"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}:{minutes:02d} ч"
    
    @staticmethod
    def format_date(date_str: str, format_from: str = '%Y-%m-%d', format_to: str = '%d.%m.%Y') -> str:
        """Форматирование даты"""
        try:
            date = datetime.strptime(date_str, format_from)
            return date.strftime(format_to)
        except:
            return date_str
    
    @staticmethod
    def format_duration(start: datetime, end: datetime) -> str:
        """Форматирование длительности"""
        duration = end - start
        total_seconds = int(duration.total_seconds())
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    @staticmethod
    def format_match_result(result: str, language: str = 'en') -> str:
        """Форматирование результата матча"""
        translations = {
            'ru': {
                'win': 'Победа 🏆',
                'loss': 'Поражение 💀',
                'draw': 'Ничья 🤝',
                'ongoing': 'В процессе ⏳',
                'cancelled': 'Отменен ❌'
            },
            'en': {
                'win': 'Win 🏆',
                'loss': 'Loss 💀',
                'draw': 'Draw 🤝',
                'ongoing': 'Ongoing ⏳',
                'cancelled': 'Cancelled ❌'
            }
        }
        
        lang_dict = translations.get(language, translations['en'])
        return lang_dict.get(result, result)
    
    @staticmethod
    def format_kda(kills: int, deaths: int, assists: int) -> str:
        """Форматирование KDA"""
        if deaths > 0:
            kda = (kills + assists) / deaths
        else:
            kda = kills + assists
        return f"{kills}/{deaths}/{assists} ({kda:.2f})"
    
    @staticmethod
    def format_kd_ratio(kills: int, deaths: int) -> str:
        """Форматирование K/D"""
        if deaths > 0:
            kd = kills / deaths
        else:
            kd = kills
        return f"{kd:.2f}"
    
    @staticmethod
    def format_rating(rating: float) -> str:
        """Форматирование рейтинга"""
        if rating >= 1.5:
            return f"🔥 {rating:.2f}"
        elif rating >= 1.0:
            return f"⭐ {rating:.2f}"
        elif rating >= 0.8:
            return f"🆗 {rating:.2f}"
        else:
            return f"📉 {rating:.2f}"
    
    @staticmethod
    def format_wn8(wn8: float) -> str:
        """Форматирование WN8"""
        if wn8 >= 3000:
            return f"👑 {wn8:.0f}"
        elif wn8 >= 2500:
            return f"💎 {wn8:.0f}"
        elif wn8 >= 2000:
            return f"⭐ {wn8:.0f}"
        elif wn8 >= 1500:
            return f"🟢 {wn8:.0f}"
        elif wn8 >= 1000:
            return f"🟡 {wn8:.0f}"
        elif wn8 >= 500:
            return f"🟠 {wn8:.0f}"
        else:
            return f"🔴 {wn8:.0f}"
    
    @staticmethod
    def format_progress(current: float, previous: float) -> str:
        """Форматирование прогресса"""
        difference = current - previous
        
        if difference > 0:
            return f"📈 +{difference:.2f}"
        elif difference < 0:
            return f"📉 {difference:.2f}"
        else:
            return f"➖ {difference:.2f}"
    
    @staticmethod
    def format_win_rate(wins: int, total: int) -> str:
        """Форматирование винрейта"""
        if total > 0:
            win_rate = (wins / total) * 100
            return f"{win_rate:.1f}%"
        return "0%"
    
    @staticmethod
    def create_table(headers: List[str], rows: List[List[Any]], column_widths: List[int] = None) -> str:
        """Создание текстовой таблицы"""
        if not rows:
            return ""
        
        if not column_widths:
            # Автоматический расчет ширины колонок
            column_widths = []
            for i in range(len(headers)):
                max_width = len(str(headers[i]))
                for row in rows:
                    if i < len(row):
                        max_width = max(max_width, len(str(row[i])))
                column_widths.append(max_width + 2)  # +2 для отступов
        
        # Создаем строку разделителя
        separator = "+" + "+".join(["-" * (w + 2) for w in column_widths]) + "+"
        
        # Создаем заголовок
        table = separator + "\n"
        header_row = "|"
        for i, header in enumerate(headers):
            header_row += f" {header:<{column_widths[i]}} |"
        table += header_row + "\n"
        table += separator + "\n"
        
        # Добавляем строки
        for row in rows:
            row_str = "|"
            for i, cell in enumerate(row):
                if i < len(column_widths):
                    row_str += f" {str(cell):<{column_widths[i]}} |"
            table += row_str + "\n"
        
        table += separator
        return table
    
    @staticmethod
    def format_stats_comparison(current_stats: Dict, previous_stats: Dict, metrics: List[str]) -> str:
        """Форматирование сравнения статистики"""
        result = "📊 Сравнение с предыдущим периодом:\n\n"
        
        for metric in metrics:
            current = current_stats.get(metric, 0)
            previous = previous_stats.get(metric, 0)
            
            if metric in ['kills', 'assists', 'deaths', 'mvp', 'matches']:
                diff = current - previous
                if diff > 0:
                    result += f"✅ {metric}: {current} (+{diff})\n"
                elif diff < 0:
                    result += f"❌ {metric}: {current} ({diff})\n"
                else:
                    result += f"➖ {metric}: {current} (без изменений)\n"
            
            elif metric in ['kd_ratio', 'kda', 'rating', 'adr', 'wn8']:
                diff = current - previous
                if diff > 0:
                    result += f"📈 {metric}: {current:.2f} (+{diff:.2f})\n"
                elif diff < 0:
                    result += f"📉 {metric}: {current:.2f} ({diff:.2f})\n"
                else:
                    result += f"➖ {metric}: {current:.2f} (без изменений)\n"
            
            elif metric in ['win_rate', 'hs_percentage']:
                diff = current - previous
                if diff > 0:
                    result += f"📈 {metric}: {current:.1f}% (+{diff:.1f}%)\n"
                elif diff < 0:
                    result += f"📉 {metric}: {current:.1f}% ({diff:.1f}%)\n"
                else:
                    result += f"➖ {metric}: {current:.1f}% (без изменений)\n"
        
        return result
    
    @staticmethod
    def format_achievements(achievements: List[Dict]) -> str:
        """Форматирование достижений"""
        if not achievements:
            return "🎖️ Достижений пока нет"
        
        result = "🏆 Ваши достижения:\n\n"
        for achievement in achievements[:10]:  # Ограничиваем 10 достижениями
            name = achievement.get('name', 'Неизвестно')
            description = achievement.get('description', '')
            unlocked = achievement.get('unlocked', False)
            date = achievement.get('date', '')
            
            if unlocked:
                if date:
                    result += f"✅ {name} - {description} ({date})\n"
                else:
                    result += f"✅ {name} - {description}\n"
            else:
                result += f"🔒 {name} - {description}\n"
        
        return result