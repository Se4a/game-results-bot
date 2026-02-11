from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database import Base

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    currency = Column(String(10))  # 'USD', 'XTR' (Telegram Stars), 'CRYPTO'
    plan_type = Column(String(50))  # '1_month', '3_months', '6_months', '12_months'
    status = Column(String(50))  # 'pending', 'completed', 'failed', 'refunded'
    transaction_id = Column(String(255), unique=True)
    payment_method = Column(String(50))  # 'crypto', 'telegram_stars', 'admin'
    provider_payment_id = Column(String(255))  # ID от платежной системы
    payment_details = Column(JSON)  # Детали платежа (адрес, хеш и т.д.)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", foreign_keys=[subscription_id])
    
    @property
    def is_confirmed(self):
        """Платеж подтвержден?"""
        return self.status == 'completed' and self.confirmed_at is not None
    
    @property
    def is_pending(self):
        """Платеж в ожидании?"""
        return self.status == 'pending'
    
    @property
    def is_failed(self):
        """Платеж провалился?"""
        return self.status == 'failed'
    
    @property
    def age_in_minutes(self):
        """Возраст платежа в минутах"""
        if not self.created_at:
            return 0
        delta = datetime.utcnow() - self.created_at
        return delta.total_seconds() / 60
    
    def confirm(self, provider_payment_id: str = None):
        """Подтвердить платеж"""
        self.status = 'completed'
        self.confirmed_at = datetime.utcnow()
        if provider_payment_id:
            self.provider_payment_id = provider_payment_id
    
    def fail(self, reason: str = None):
        """Отметить платеж как проваленный"""
        self.status = 'failed'
        if reason:
            self.payment_details = self.payment_details or {}
            self.payment_details['failure_reason'] = reason
    
    def refund(self):
        """Вернуть платеж"""
        self.status = 'refunded'
        self.refunded_at = datetime.utcnow()
    
    @property
    def stars_amount(self):
        """Количество Stars для Telegram Stars"""
        if self.currency == 'XTR':
            return int(self.amount)
        return None
    
    @property
    def usd_amount(self):
        """Сумма в USD"""
        if self.currency == 'USD':
            return self.amount
        # Конвертация Stars в USD (1 Star = $0.01)
        elif self.currency == 'XTR':
            return self.amount * 0.01
        # Для криптовалюты - примерная стоимость
        elif self.currency == 'CRYPTO':
            return self.payment_details.get('usd_value', 0) if self.payment_details else 0
        return 0
    
    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount} {self.currency}, status={self.status})>"
