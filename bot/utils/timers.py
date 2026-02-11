import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from bot.database import async_session
from sqlalchemy import select, and_
from bot.models.match import Match
from bot.models.user import User
from bot.models.subscription import Subscription
from bot.services.notification_service import NotificationService

class TimerManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.notification_service = NotificationService(bot)
        self.running = True
    
    async def check_subscriptions(self):
        """Check and update subscription statuses"""
        while self.running:
            try:
                async with async_session() as session:
                    # Get expiring subscriptions (within 3 days)
                    result = await session.execute(
                        select(Subscription).where(
                            and_(
                                Subscription.is_active == True,
                                Subscription.end_date <= datetime.utcnow() + timedelta(days=3),
                                Subscription.end_date > datetime.utcnow()
                            )
                        )
                    )
                    expiring_subs = result.scalars().all()
                    
                    for sub in expiring_subs:
                        # Get user info
                        user_result = await session.execute(
                            select(User).where(User.id == sub.user_id)
                        )
                        user = user_result.scalar_one_or_none()
                        
                        if user:
                            days_left = (sub.end_date - datetime.utcnow()).days
                            await self.notification_service.send_subscription_reminder(
                                user.telegram_id,
                                user.language,
                                days_left
                            )
                    
                    # Deactivate expired subscriptions
                    result = await session.execute(
                        select(Subscription).where(
                            and_(
                                Subscription.is_active == True,
                                Subscription.end_date <= datetime.utcnow()
                            )
                        )
                    )
                    expired_subs = result.scalars().all()
                    
                    for sub in expired_subs:
                        sub.is_active = False
                    
                    await session.commit()
                    
            except Exception as e:
                print(f"Error in subscription check: {e}")
            
            await asyncio.sleep(3600)  # Check every hour
    
    async def reset_daily_limits(self):
        """Reset daily match limits at midnight UTC"""
        while self.running:
            try:
                now = datetime.utcnow()
                # Calculate time until next midnight
                next_midnight = (now + timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                wait_seconds = (next_midnight - now).total_seconds()
                
                # Wait until midnight
                await asyncio.sleep(wait_seconds)
                
                # Reset daily stats
                async with async_session() as session:
                    await session.execute(
                        "UPDATE daily_stats SET matches_used = 0, last_reset = :now",
                        {'now': datetime.utcnow()}
                    )
                    await session.commit()
                    
            except Exception as e:
                print(f"Error resetting daily limits: {e}")
                await asyncio.sleep(60)  # Retry after error
    
    async def update_live_matches(self):
        """Update live match statistics every 3 minutes"""
        while self.running:
            try:
                async with async_session() as session:
                    # Get all tracked live matches
                    result = await session.execute(
                        select(Match).where(
                            and_(
                                Match.is_tracked == True,
                                Match.is_completed == False
                            )
                        )
                    )
                    live_matches = result.scalars().all()
                    
                    for match in live_matches:
                        # Update match statistics
                        # This would call game-specific APIs
                        pass
                    
            except Exception as e:
                print(f"Error updating live matches: {e}")
            
            await asyncio.sleep(180)  # Update every 3 minutes
    
    async def start_all(self):
        """Start all timer tasks"""
        tasks = [
            self.check_subscriptions(),
            self.reset_daily_limits(),
            self.update_live_matches()
        ]
        await asyncio.gather(*tasks)

async def start_timers(bot: Bot):
    """Start timer manager"""
    manager = TimerManager(bot)
    asyncio.create_task(manager.start_all())