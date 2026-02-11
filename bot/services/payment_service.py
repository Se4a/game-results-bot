import aiohttp
from datetime import datetime, timedelta
from aiogram.types import LabeledPrice
from bot.config import config
import json

class PaymentService:
    def __init__(self):
        self.crypto_address = config.CRYPTO_ADDRESS
        self.stars_to_usd_rate = config.STARS_TO_USD_RATE
    
    def get_stars_price(self, plan_type: str) -> int:
        """Получить цену в Stars для плана подписки"""
        return config.SUBSCRIPTION_PRICES_STARS.get(plan_type, 99)
    
    def get_usd_price(self, plan_type: str) -> float:
        """Получить цену в USD для плана подписки"""
        return config.SUBSCRIPTION_PRICES_USD.get(plan_type, 0.99)
    
    def create_stars_invoice(self, plan_type: str, user_id: int):
        """Создать инвойс для оплаты Telegram Stars"""
        stars_price = self.get_stars_price(plan_type)
        usd_price = self.get_usd_price(plan_type)
        
        # Генерируем уникальный payload
        payload = f"subscription:{plan_type}:{user_id}:{int(datetime.now().timestamp())}"
        
        # Создаем описание
        descriptions = {
            '1_month': "1 month subscription",
            '3_months': "3 months subscription",
            '6_months': "6 months subscription",
            '12_months': "12 months subscription"
        }
        
        description = descriptions.get(plan_type, "Game Results Bot Subscription")
        
        # Создаем цены для инвойса (в минимальных единицах, для Stars это 1/100)
        prices = [LabeledPrice(label=description, amount=stars_price * 100)]
        
        return {
            'title': f"Subscription: {plan_type.replace('_', ' ')}",
            'description': description,
            'payload': payload,
            'provider_token': None,  # Для Stars провайдер не нужен
            'currency': 'XTR',  # Telegram Stars currency code
            'prices': prices,
            'start_parameter': plan_type,
            'need_email': False,
            'need_phone_number': False,
            'need_shipping_address': False,
            'is_flexible': False
        }
    
    async def process_crypto_payment(self, user_id: int, amount: float, plan_type: str) -> dict:
        """Process cryptocurrency payment"""
        # In production, integrate with zerocryptopay.com API
        # For now, generate a payment address
        
        payment_data = {
            'user_id': user_id,
            'amount': amount,
            'currency': 'USD',
            'plan_type': plan_type,
            'crypto_address': self.crypto_address,
            'status': 'pending',
            'transaction_id': f'crypto_{user_id}_{int(datetime.now().timestamp())}',
            'created_at': datetime.now().isoformat(),
            'usd_amount': amount,
            'stars_amount': int(amount / self.stars_to_usd_rate)
        }
        
        return payment_data
    
    async def process_stars_payment(self, user_id: int, plan_type: str) -> dict:
        """Process Telegram Stars payment"""
        stars_price = self.get_stars_price(plan_type)
        usd_price = self.get_usd_price(plan_type)
        
        payment_data = {
            'user_id': user_id,
            'amount': stars_price,
            'currency': 'XTR',
            'plan_type': plan_type,
            'status': 'pending',
            'transaction_id': f'stars_{user_id}_{int(datetime.now().timestamp())}',
            'created_at': datetime.now().isoformat(),
            'usd_amount': usd_price,
            'stars_amount': stars_price,
            'provider_payment_charge_id': None  # Will be filled after successful payment
        }
        
        return payment_data
    
    async def verify_stars_payment(self, provider_payment_charge_id: str, telegram_payment_charge_id: str) -> bool:
        """Verify Telegram Stars payment"""
        # In production, this would verify the payment with Telegram
        # For now, we assume all Telegram payments are valid
        # In a real implementation, you would use Telegram Bot API to verify
        
        if provider_payment_charge_id and telegram_payment_charge_id:
            return True
        return False
    
    async def check_payment_status(self, transaction_id: str) -> dict:
        """Check if payment was confirmed"""
        # This would query zerocryptopay.com API for crypto or Telegram API for Stars
        # For now, simulate payment confirmation
        
        # Check if it's a Stars payment
        if transaction_id.startswith('stars_'):
            # For Stars, we need to wait for pre_checkout_query and successful_payment
            # This is handled by the bot's handlers
            return {
                'status': 'pending',
                'confirmed_at': None
            }
        else:
            # For crypto, simulate confirmation after 2 minutes
            return {
                'status': 'completed',
                'confirmed_at': datetime.now().isoformat()
            }
    
    async def create_subscription(self, user_id: int, plan_type: str, payment_method: str) -> dict:
        """Create subscription based on plan type"""
        
        start_date = datetime.now()
        duration_days = config.SUBSCRIPTION_DURATIONS.get(plan_type, 30)
        end_date = start_date + timedelta(days=duration_days)
        
        subscription = {
            'user_id': user_id,
            'plan_type': plan_type,
            'start_date': start_date,
            'end_date': end_date,
            'payment_method': payment_method,
            'is_active': True,
            'price_usd': self.get_usd_price(plan_type),
            'price_stars': self.get_stars_price(plan_type)
        }
        
        return subscription