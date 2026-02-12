from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.localization import get_text
from bot.config import config

def get_settings_main_keyboard(language: str) -> InlineKeyboardMarkup:
    """Главное меню настроек"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "🌍 Язык / Language",
            callback_data='settings_language'
        ),
        InlineKeyboardButton(
            "🎮 Настройки игр",
            callback_data='settings_games'
        ),
        InlineKeyboardButton(
            "🔔 Уведомления",
            callback_data='settings_notifications'
        ),
        InlineKeyboardButton(
            "📊 Статистика и данные",
            callback_data='settings_privacy'
        ),
        InlineKeyboardButton(
            "⚡ Автообновление",
            callback_data='settings_auto_update'
        ),
        InlineKeyboardButton(
            "🎨 Внешний вид",
            callback_data='settings_appearance'
        ),
        InlineKeyboardButton(
            "🛡️ Безопасность",
            callback_data='settings_security'
        ),
        InlineKeyboardButton(
            "🗑️ Удаление данных",
            callback_data='settings_data_deletion'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_main'
        )
    )
    
    return keyboard

def get_language_selection_keyboard(language: str) -> InlineKeyboardMarkup:
    """Выбор языка"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    
    languages = [
        ('🇷🇺', 'Русский', 'ru'),
        ('🇺🇸', 'English', 'en'),
        ('🇺🇦', 'Українська', 'uk'),
        ('🇩🇪', 'Deutsch', 'de'),
        ('🇫🇷', 'Français', 'fr'),
        ('🇮🇹', 'Italiano', 'it'),
        ('🇵🇱', 'Polski', 'pl'),
        ('🇳🇱', 'Nederlands', 'nl'),
        ('🇨🇳', '中文', 'zh'),
        ('🇰🇷', '한국어', 'ko'),
        ('🇵🇹', 'Português', 'pt'),
        ('🇪🇸', 'Español', 'es')
    ]
    
    for flag, name, code in languages:
        is_current = " ✅" if code == language else ""
        keyboard.add(
            InlineKeyboardButton(
                f"{flag} {name}{is_current}",
                callback_data=f'set_language_{code}'
            )
        )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_game_settings_keyboard(language: str) -> InlineKeyboardMarkup:
    """Настройки игр"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    games = [
        ('🎯', 'CS:GO', 'csgo'),
        ('⚔️', 'Dota 2', 'dota2'),
        ('🔫', 'Valorant', 'valorant'),
        ('🏆', 'League of Legends', 'lol'),
        ('🎖️', 'World of Tanks', 'wot'),
        ('🌍', 'PUBG', 'pubg')
    ]
    
    for emoji, name, game_code in games:
        keyboard.add(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=f'game_settings_{game_code}'
            )
        )
    
    # Общие настройки для всех игр
    keyboard.add(
        InlineKeyboardButton(
            "⚙️ Общие настройки игр",
            callback_data='common_game_settings'
        )
    )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_specific_game_settings_keyboard(language: str, game: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки конкретной игры"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    auto_update = settings.get('auto_update', True)
    compare_depth = settings.get('compare_depth', 3)
    detailed_stats = settings.get('detailed_stats', True)
    notifications = settings.get('notifications', True)
    
    buttons = [
        InlineKeyboardButton(
            f"{'🔄' if auto_update else '⏸️'} Автообновление: {'Вкл' if auto_update else 'Выкл'}",
            callback_data=f'toggle_auto_update_{game}'
        ),
        InlineKeyboardButton(
            f"📊 Глубина сравнения: {compare_depth} игр",
            callback_data=f'set_compare_depth_{game}'
        ),
        InlineKeyboardButton(
            f"{'📈' if detailed_stats else '📉'} Детальная статистика: {'Вкл' if detailed_stats else 'Выкл'}",
            callback_data=f'toggle_detailed_stats_{game}'
        ),
        InlineKeyboardButton(
            f"{'🔔' if notifications else '🔕'} Уведомления: {'Вкл' if notifications else 'Выкл'}",
            callback_data=f'toggle_notifications_{game}'
        ),
        InlineKeyboardButton(
            "⚙️ Дополнительные настройки",
            callback_data=f'advanced_settings_{game}'
        ),
        InlineKeyboardButton(
            "🔄 Синхронизировать данные",
            callback_data=f'sync_game_data_{game}'
        ),
        InlineKeyboardButton(
            "🗑️ Очистить историю",
            callback_data=f'clear_game_history_{game}'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка смены аккаунта
    keyboard.add(
        InlineKeyboardButton(
            "🔄 Сменить аккаунт",
            callback_data=f'change_game_account_{game}'
        )
    )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_game_settings'
        )
    )
    
    return keyboard

def get_compare_depth_keyboard(language: str, game: str, current_depth: int) -> InlineKeyboardMarkup:
    """Выбор глубины сравнения"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    
    depths = [1, 2, 3, 5, 10, 15, 20]
    
    for depth in depths:
        is_current = " ✅" if depth == current_depth else ""
        keyboard.add(
            InlineKeyboardButton(
                f"{depth} игр{is_current}",
                callback_data=f'set_depth_{game}_{depth}'
            )
        )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'back_to_game_settings_{game}'
        )
    )
    
    return keyboard

def get_notification_settings_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки уведомлений"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    match_start = settings.get('match_start', True)
    match_end = settings.get('match_end', True)
    live_updates = settings.get('live_updates', True)
    achievements = settings.get('achievements', True)
    promotions = settings.get('promotions', True)
    subscription = settings.get('subscription', True)
    
    buttons = [
        InlineKeyboardButton(
            f"{'🎮' if match_start else '⏸️'} Начало матча: {'Вкл' if match_start else 'Выкл'}",
            callback_data='toggle_match_start_notifications'
        ),
        InlineKeyboardButton(
            f"{'🏆' if match_end else '📭'} Конец матча: {'Вкл' if match_end else 'Выкл'}",
            callback_data='toggle_match_end_notifications'
        ),
        InlineKeyboardButton(
            f"{'🔄' if live_updates else '⏹️'} Live-обновления: {'Вкл' if live_updates else 'Выкл'}",
            callback_data='toggle_live_updates'
        ),
        InlineKeyboardButton(
            f"{'🎖️' if achievements else '📭'} Достижения: {'Вкл' if achievements else 'Выкл'}",
            callback_data='toggle_achievement_notifications'
        ),
        InlineKeyboardButton(
            f"{'🎁' if promotions else '📭'} Акции: {'Вкл' if promotions else 'Выкл'}",
            callback_data='toggle_promotion_notifications'
        ),
        InlineKeyboardButton(
            f"{'💎' if subscription else '📭'} Подписка: {'Вкл' if subscription else 'Выкл'}",
            callback_data='toggle_subscription_notifications'
        ),
        InlineKeyboardButton(
            "⏰ Настройка времени",
            callback_data='set_notification_time'
        ),
        InlineKeyboardButton(
            "🔕 Режим 'Не беспокоить'",
            callback_data='toggle_do_not_disturb'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_privacy_settings_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки конфиденциальности и данных"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    public_profile = settings.get('public_profile', False)
    share_stats = settings.get('share_stats', True)
    analytics = settings.get('analytics', True)
    personalized_ads = settings.get('personalized_ads', False)
    
    buttons = [
        InlineKeyboardButton(
            f"{'🌐' if public_profile else '🔒'} Публичный профиль: {'Вкл' if public_profile else 'Выкл'}",
            callback_data='toggle_public_profile'
        ),
        InlineKeyboardButton(
            f"{'📊' if share_stats else '🚫'} Общая статистика: {'Вкл' if share_stats else 'Выкл'}",
            callback_data='toggle_share_stats'
        ),
        InlineKeyboardButton(
            f"{'📈' if analytics else '📉'} Аналитика: {'Вкл' if analytics else 'Выкл'}",
            callback_data='toggle_analytics'
        ),
        InlineKeyboardButton(
            f"{'🎯' if personalized_ads else '📢'} Персонализированные предложения: {'Вкл' if personalized_ads else 'Выкл'}",
            callback_data='toggle_personalized_ads'
        ),
        InlineKeyboardButton(
            "👁️ Кто видит мои данные",
            callback_data='data_visibility'
        ),
        InlineKeyboardButton(
            "📥 Экспорт данных",
            callback_data='export_data'
        ),
        InlineKeyboardButton(
            "🗑️ Удалить данные",
            callback_data='delete_data_confirm'
        ),
        InlineKeyboardButton(
            "🛡️ Политика конфиденциальности",
            callback_data='privacy_policy'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_auto_update_settings_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки автообновления"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    enabled = settings.get('enabled', True)
    interval = settings.get('interval', 180)
    only_when_active = settings.get('only_when_active', True)
    mobile_data = settings.get('mobile_data', False)
    
    intervals = [60, 120, 180, 300, 600]  # секунды
    
    buttons = [
        InlineKeyboardButton(
            f"{'🔄' if enabled else '⏸️'} Автообновление: {'Вкл' if enabled else 'Выкл'}",
            callback_data='toggle_auto_update'
        ),
        InlineKeyboardButton(
            f"⏱️ Интервал: {interval} сек",
            callback_data='set_update_interval'
        ),
        InlineKeyboardButton(
            f"{'🎮' if only_when_active else '📱'} Только во время игры: {'Вкл' if only_when_active else 'Выкл'}",
            callback_data='toggle_only_when_active'
        ),
        InlineKeyboardButton(
            f"{'📶' if mobile_data else 'WiFi'} Обновление по мобильным данным: {'Вкл' if mobile_data else 'Выкл'}",
            callback_data='toggle_mobile_data_updates'
        ),
        InlineKeyboardButton(
            "⚡ Быстрое обновление",
            callback_data='fast_update_settings'
        ),
        InlineKeyboardButton(
            "📊 Статистика обновлений",
            callback_data='update_statistics'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_appearance_settings_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки внешнего вида"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    theme = settings.get('theme', 'auto')
    compact_mode = settings.get('compact_mode', False)
    animations = settings.get('animations', True)
    emoji_mode = settings.get('emoji_mode', True)
    
    buttons = [
        InlineKeyboardButton(
            f"🎨 Тема: {'Авто' if theme == 'auto' else 'Светлая' if theme == 'light' else 'Темная'}",
            callback_data='change_theme'
        ),
        InlineKeyboardButton(
            f"{'📱' if compact_mode else '🖥️'} Компактный режим: {'Вкл' if compact_mode else 'Выкл'}",
            callback_data='toggle_compact_mode'
        ),
        InlineKeyboardButton(
            f"{'✨' if animations else '⚡'} Анимации: {'Вкл' if animations else 'Выкл'}",
            callback_data='toggle_animations'
        ),
        InlineKeyboardButton(
            f"{'😊' if emoji_mode else '📊'} Emoji: {'Вкл' if emoji_mode else 'Выкл'}",
            callback_data='toggle_emoji_mode'
        ),
        InlineKeyboardButton(
            "🖼️ Настроить отображение статистики",
            callback_data='customize_stats_display'
        ),
        InlineKeyboardButton(
            "📏 Размер текста",
            callback_data='text_size_settings'
        ),
        InlineKeyboardButton(
            "🎯 Цветовые схемы",
            callback_data='color_schemes'
        ),
        InlineKeyboardButton(
            "🔄 Сбросить настройки",
            callback_data='reset_appearance'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_security_settings_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Настройки безопасности"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    two_factor = settings.get('two_factor', False)
    login_alerts = settings.get('login_alerts', True)
    session_management = settings.get('session_management', True)
    
    buttons = [
        InlineKeyboardButton(
            f"{'🔐' if two_factor else '🔓'} Двухфакторная аутентификация: {'Вкл' if two_factor else 'Выкл'}",
            callback_data='toggle_two_factor'
        ),
        InlineKeyboardButton(
            f"{'🔔' if login_alerts else '🔕'} Оповещения о входе: {'Вкл' if login_alerts else 'Выкл'}",
            callback_data='toggle_login_alerts'
        ),
        InlineKeyboardButton(
            "📱 Управление сессиями",
            callback_data='session_management'
        ),
        InlineKeyboardButton(
            "👁️ История активности",
            callback_data='activity_history'
        ),
        InlineKeyboardButton(
            "🚫 Заблокированные пользователи",
            callback_data='blocked_users'
        ),
        InlineKeyboardButton(
            "📧 Смена email",
            callback_data='change_email'
        ),
        InlineKeyboardButton(
            "🔑 Смена пароля",
            callback_data='change_password'
        ),
        InlineKeyboardButton(
            "🛡️ Проверка безопасности",
            callback_data='security_check'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_data_deletion_keyboard(language: str) -> InlineKeyboardMarkup:
    """Удаление данных"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "🗑️ Удалить историю матчей",
            callback_data='delete_match_history'
        ),
        InlineKeyboardButton(
            "🚫 Удалить игровые аккаунты",
            callback_data='delete_game_accounts'
        ),
        InlineKeyboardButton(
            "📊 Удалить статистику",
            callback_data='delete_statistics'
        ),
        InlineKeyboardButton(
            "💬 Удалить сообщения",
            callback_data='delete_messages'
        ),
        InlineKeyboardButton(
            "👤 Удалить аккаунт полностью",
            callback_data='delete_account_confirm'
        ),
        InlineKeyboardButton(
            "📥 Скачать все данные",
            callback_data='download_all_data'
        ),
        InlineKeyboardButton(
            "📜 Политика данных",
            callback_data='data_policy'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_settings'
        )
    )
    
    return keyboard

def get_confirmation_keyboard(language: str, action: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения действия"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "✅ Да, подтверждаю",
            callback_data=f'confirm_{action}'
        ),
        InlineKeyboardButton(
            "❌ Нет, отмена",
            callback_data=f'cancel_{action}'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'back_before_{action}'
        )
    )
    
    return keyboard
