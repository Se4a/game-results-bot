def get_game_detailed_menu(game: str, language: str = 'en') -> InlineKeyboardMarkup:
    """Меню с опциями детальной статистики"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "📊 Полная статистика",
            callback_data=f'complete_stats_{game}'
        ),
        InlineKeyboardButton(
            "🎮 Live отслеживание",
            callback_data=f'live_track_{game}'
        ),
        InlineKeyboardButton(
            "📈 История матчей",
            callback_data=f'match_history_{game}'
        ),
        InlineKeyboardButton(
            "⚙️ Настройки отслеживания",
            callback_data=f'tracking_settings_{game}'
        ),
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_games'
        )
    ]
    
    keyboard.add(*buttons)
    return keyboard