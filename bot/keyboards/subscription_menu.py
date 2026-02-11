from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.localization import get_text
from bot.config import config
from datetime import datetime

def get_subscription_status_keyboard(language: str, has_active_sub: bool, days_left: int = 0) -> InlineKeyboardMarkup:
    """Клавиатура статуса подписки"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    if has_active_sub:
        buttons = [
            InlineKeyboardButton(
                "🔄 Продлить подписку",
                callback_data='renew_subscription'
            ),
            InlineKeyboardButton(
                "📋 История платежей",
                callback_data='payment_history'
            ),
            InlineKeyboardButton(
                "❌ Отменить подписку",
                callback_data='cancel_subscription'
            )
        ]
    else:
        buttons = [
            InlineKeyboardButton(
                "💎 Купить подписку",
                callback_data='buy_subscription'
            ),
            InlineKeyboardButton(
                "💰 Цены и тарифы",
                callback_data='pricing_info'
            ),
            InlineKeyboardButton(
                "🎁 Промокод",
                callback_data='use_promo'
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

def get_subscription_plans_keyboard(language: str, current_plan: str = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора плана подписки"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    plans = [
        {
            'id': '1_month',
            'name': get_text('subscription.month', language),
            'price_usd': 0.99,
            'price_stars': 99,
            'emoji': '📅'
        },
        {
            'id': '3_months',
            'name': f"3 {get_text('subscription.months', language)}",
            'price_usd': 2.50,
            'price_stars': 250,
            'emoji': '💰',
            'saving': '16%'
        },
        {
            'id': '6_months',
            'name': f"6 {get_text('subscription.months', language)}",
            'price_usd': 5.00,
            'price_stars': 500,
            'emoji': '💎',
            'saving': '16%'
        },
        {
            'id': '12_months',
            'name': f"12 {get_text('subscription.months', language)}",
            'price_usd': 10.00,
            'price_stars': 1000,
            'emoji': '👑',
            'saving': '16%'
        }
    ]
    
    for plan in plans:
        text = f"{plan['emoji']} {plan['name']} - ${plan['price_usd']} ({plan['price_stars']} ⭐)"
        
        if plan.get('saving'):
            text += f" (экономия {plan['saving']})"
        
        if current_plan == plan['id']:
            text = f"✅ {text} (текущий)"
        
        keyboard.add(
            InlineKeyboardButton(
                text,
                callback_data=f'sub_{plan["id"]}'
            )
        )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription'
        )
    )
    
    return keyboard

def get_payment_methods_keyboard(language: str, plan_id: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора способа оплаты"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Получаем цену плана
    prices = {
        '1_month': {'usd': 0.99, 'stars': 99},
        '3_months': {'usd': 2.50, 'stars': 250},
        '6_months': {'usd': 5.00, 'stars': 500},
        '12_months': {'usd': 10.00, 'stars': 1000}
    }
    
    plan_price = prices.get(plan_id, prices['1_month'])
    
    buttons = [
        InlineKeyboardButton(
            f"⭐ Telegram Stars ({plan_price['stars']} ⭐)",
            callback_data=f'pay_stars:{plan_id}'
        ),
        InlineKeyboardButton(
            f"₿ Cryptocurrency (${plan_price['usd']})",
            callback_data=f'pay_crypto:{plan_id}'
        ),
        InlineKeyboardButton(
            "💳 Другие способы",
            callback_data=f'pay_other:{plan_id}'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'back_to_plans'
        )
    )
    
    return keyboard

def get_crypto_payment_keyboard(language: str, plan_id: str, crypto_address: str) -> InlineKeyboardMarkup:
    """Клавиатура для оплаты криптовалютой"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    prices = {
        '1_month': 0.99,
        '3_months': 2.50,
        '6_months': 5.00,
        '12_months': 10.00
    }
    
    price = prices.get(plan_id, 0.99)
    
    buttons = [
        InlineKeyboardButton(
            "📋 Скопировать адрес",
            callback_data=f'copy_address:{crypto_address}'
        ),
        InlineKeyboardButton(
            "✅ Я оплатил",
            callback_data=f'confirm_crypto_payment:{plan_id}'
        ),
        InlineKeyboardButton(
            "🔄 Проверить платеж",
            callback_data=f'check_crypto_payment:{plan_id}'
        ),
        InlineKeyboardButton(
            "❓ Помощь",
            callback_data='crypto_payment_help'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'back_to_payment_methods:{plan_id}'
        )
    )
    
    return keyboard

def get_stars_payment_keyboard(language: str, plan_id: str, stars_amount: int) -> InlineKeyboardMarkup:
    """Клавиатура для оплаты Telegram Stars"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Создаем инвойс для оплаты Stars
    invoice_payload = f"subscription:{plan_id}:{int(datetime.now().timestamp())}"
    
    buttons = [
        InlineKeyboardButton(
            f"💳 Оплатить {stars_amount} Stars",
            pay=True
        ),
        InlineKeyboardButton(
            "❓ Как купить Stars?",
            callback_data='stars_help'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'back_to_payment_methods:{plan_id}'
        )
    )
    
    return keyboard

def get_subscription_management_keyboard(language: str) -> InlineKeyboardMarkup:
    """Клавиатура управления подпиской"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "🔄 Продлить",
            callback_data='extend_subscription'
        ),
        InlineKeyboardButton(
            "📊 Статистика использования",
            callback_data='usage_stats'
        ),
        InlineKeyboardButton(
            "📋 Детали подписки",
            callback_data='subscription_details'
        ),
        InlineKeyboardButton(
            "🔔 Настройка уведомлений",
            callback_data='subscription_notifications'
        ),
        InlineKeyboardButton(
            "❌ Отменить подписку",
            callback_data='cancel_subscription_confirm'
        ),
        InlineKeyboardButton(
            "💬 Поддержка",
            callback_data='subscription_support'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription'
        )
    )
    
    return keyboard

def get_cancel_subscription_keyboard(language: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения отмены подписки"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "✅ Да, отменить",
            callback_data='confirm_cancel_subscription'
        ),
        InlineKeyboardButton(
            "❌ Нет, оставить",
            callback_data='keep_subscription'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription_management'
        )
    )
    
    return keyboard

def get_payment_history_keyboard(language: str, page: int = 1, has_next: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура истории платежей"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    
    navigation_buttons = []
    
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                "◀️ Назад",
                callback_data=f'payment_history_page:{page-1}'
            )
        )
    
    navigation_buttons.append(
        InlineKeyboardButton(
            f"📄 {page}",
            callback_data='current_page'
        )
    )
    
    if has_next:
        navigation_buttons.append(
            InlineKeyboardButton(
                "Вперед ▶️",
                callback_data=f'payment_history_page:{page+1}'
            )
        )
    
    if navigation_buttons:
        keyboard.add(*navigation_buttons)
    
    # Дополнительные кнопки
    keyboard.add(
        InlineKeyboardButton(
            "📥 Экспорт в CSV",
            callback_data='export_payments_csv'
        ),
        InlineKeyboardButton(
            "🧾 Получить чек",
            callback_data='get_payment_receipt'
        )
    )
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription_management'
        )
    )
    
    return keyboard

def get_subscription_notifications_keyboard(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Клавиатура настроек уведомлений подписки"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Текущие настройки
    expiry_notifications = settings.get('expiry_notifications', True)
    payment_notifications = settings.get('payment_notifications', True)
    promotion_notifications = settings.get('promotion_notifications', True)
    
    buttons = [
        InlineKeyboardButton(
            f"{'🔔' if expiry_notifications else '🔕'} Уведомления об окончании",
            callback_data='toggle_expiry_notifications'
        ),
        InlineKeyboardButton(
            f"{'💳' if payment_notifications else '🚫'} Уведомления о платежах",
            callback_data='toggle_payment_notifications'
        ),
        InlineKeyboardButton(
            f"{'🎁' if promotion_notifications else '📭'} Промо-уведомления",
            callback_data='toggle_promotion_notifications'
        ),
        InlineKeyboardButton(
            "⏰ Настроить время уведомлений",
            callback_data='configure_notification_time'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription_management'
        )
    )
    
    return keyboard

def get_promo_code_keyboard(language: str) -> InlineKeyboardMarkup:
    """Клавиатура для ввода промокода"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "🎁 Ввести промокод",
            callback_data='enter_promo_code'
        ),
        InlineKeyboardButton(
            "📜 Активные промокоды",
            callback_data='active_promo_codes'
        ),
        InlineKeyboardButton(
            "🎯 Получить промокод",
            callback_data='get_promo_code'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data='back_to_subscription'
        )
    )
    
    return keyboard

def get_admin_subscription_keyboard(language: str, user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура админ-управления подпиской"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            "♾️ Бесконечная подписка",
            callback_data=f'admin_sub_infinite:{user_id}'
        ),
        InlineKeyboardButton(
            "📅 1 месяц",
            callback_data=f'admin_sub_1month:{user_id}'
        ),
        InlineKeyboardButton(
            "📅 3 месяца",
            callback_data=f'admin_sub_3months:{user_id}'
        ),
        InlineKeyboardButton(
            "📅 6 месяцев",
            callback_data=f'admin_sub_6months:{user_id}'
        ),
        InlineKeyboardButton(
            "📅 12 месяцев",
            callback_data=f'admin_sub_12months:{user_id}'
        ),
        InlineKeyboardButton(
            "❌ Отменить подписку",
            callback_data=f'admin_sub_cancel:{user_id}'
        ),
        InlineKeyboardButton(
            "📊 Статистика пользователя",
            callback_data=f'admin_user_stats:{user_id}'
        ),
        InlineKeyboardButton(
            "💰 История платежей",
            callback_data=f'admin_payment_history:{user_id}'
        )
    ]
    
    keyboard.add(*buttons)
    
    # Кнопка возврата
    keyboard.add(
        InlineKeyboardButton(
            get_text('back', language),
            callback_data=f'admin_back_to_user:{user_id}'
        )
    )
    
    return keyboard