from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.localization import get_text
from bot.config import config

def get_main_menu(language: str = 'en') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )
    
    buttons = [
        KeyboardButton(get_text('menu.csgo', language)),
        KeyboardButton(get_text('menu.dota', language)),
        KeyboardButton(get_text('menu.valorant', language)),
        KeyboardButton(get_text('menu.lol', language)),
        KeyboardButton(get_text('menu.wot', language)),
        KeyboardButton(get_text('menu.pubg', language)),
        KeyboardButton(get_text('menu.settings', language)),
        KeyboardButton(get_text('menu.subscription', language)),
        KeyboardButton(get_text('menu.donate', language)),
    ]
    
    keyboard.add(*buttons)
    return keyboard

def get_games_menu(language: str = 'en') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            get_text('games.csgo', language),
            callback_data='game_csgo'
        ),
        InlineKeyboardButton(
            get_text('games.dota', language),
            callback_data='game_dota'
        ),
        InlineKeyboardButton(
            get_text('games.valorant', language),
            callback_data='game_valorant'
        ),
        InlineKeyboardButton(
            get_text('games.lol', language),
            callback_data='game_lol'
        ),
        InlineKeyboardButton(
            get_text('games.wot', language),
            callback_data='game_wot'
        ),
        InlineKeyboardButton(
            get_text('games.pubg', language),
            callback_data='game_pubg'
        ),
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_main'
        )
    ]
    
    keyboard.add(*buttons)
    return keyboard

def get_subscription_menu(language: str = 'en', has_active_sub: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    if not has_active_sub:
        buttons = [
            InlineKeyboardButton(
                f"1 {get_text('subscription.month', language)} - $0.99 / 99 ⭐",
                callback_data='sub_1_month'
            ),
            InlineKeyboardButton(
                f"3 {get_text('subscription.months', language)} - $2.50 / 250 ⭐",
                callback_data='sub_3_months'
            ),
            InlineKeyboardButton(
                f"6 {get_text('subscription.months', language)} - $5.00 / 500 ⭐",
                callback_data='sub_6_months'
            ),
            InlineKeyboardButton(
                f"12 {get_text('subscription.months', language)} - $10.00 / 1000 ⭐",
                callback_data='sub_12_months'
            ),
        ]
        keyboard.add(*buttons)
    
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_main'
        )
    )
    
    return keyboard

def get_payment_method_menu(language: str = 'en', plan_type: str = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    if plan_type:
        # Получаем цену в Stars для выбранного плана
        stars_price = config.SUBSCRIPTION_PRICES_STARS.get(plan_type, 99)
        usd_price = config.SUBSCRIPTION_PRICES_USD.get(plan_type, 0.99)
        
        buttons = [
            InlineKeyboardButton(
                f"⭐ Telegram Stars ({stars_price} ⭐ = ${usd_price})",
                callback_data=f'pay_stars:{plan_type}'
            ),
            InlineKeyboardButton(
                f"₿ Cryptocurrency (${usd_price})",
                callback_data=f'pay_crypto:{plan_type}'
            ),
        ]
        keyboard.add(*buttons)
    
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription'
        )
    )
    
    return keyboard

def get_stars_payment_keyboard(language: str = 'en', plan_type: str = None) -> InlineKeyboardMarkup:
    """Клавиатура для оплаты Telegram Stars"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    if plan_type:
        stars_price = config.SUBSCRIPTION_PRICES_STARS.get(plan_type, 99)
        
        # Создаем инвойс для оплаты Stars
        invoice_payload = f"subscription:{plan_type}:{int(datetime.now().timestamp())}"
        
        prices = [LabeledPrice(label=f"Subscription {plan_type}", amount=stars_price * 100)]
        
        buttons = [
            InlineKeyboardButton(
                f"💳 Оплатить {stars_price} Stars",
                pay=True
            ),
            InlineKeyboardButton(
                get_text('back', language),
                callback_data=f'back_to_payment:{plan_type}'
            )
        ]
        keyboard.add(*buttons)
    
    return keyboard
    
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
