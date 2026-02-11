from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from bot.database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    is_active = Column(Boolean, default=False)
    plan_type = Column(String(50))  # 'monthly', '3months', '6months', 'yearly', 'infinite'
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    payment_method = Column(String(50))  # 'crypto', 'telegram_stars', 'admin_grant'
    transaction_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscription")
    
    @property
    def days_left(self):
        """Количество дней до окончания подписки"""
        if not self.end_date:
            return 0
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)
    
    @property
    def is_expired(self):
        """Проверка, истекла ли подписка"""
        if not self.end_date:
            return True
        return datetime.utcnow() > self.end_date
    
    def renew(self, plan_type: str, payment_method: str):
        """Продлить подписку"""
        from datetime import datetime, timedelta
        
        durations = {
            '1_month': 30,
            '3_months': 90,
            '6_months': 180,
            '12_months': 365,
            'infinite': 36500  # 100 лет
        }
        
        days = durations.get(plan_type, 30)
        
        if self.end_date and self.end_date > datetime.utcnow():
            # Продлеваем существующую
            self.end_date = self.end_date + timedelta(days=days)
        else:
            # Новая подписка
            self.start_date = datetime.utcnow()
            self.end_date = datetime.utcnow() + timedelta(days=days)
        
        self.plan_type = plan_type
        self.payment_method = payment_method
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def cancel(self):
        """Отменить подписку"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, active={self.is_active}, type={self.plan_type})>"
