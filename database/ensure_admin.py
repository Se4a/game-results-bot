import asyncio
from bot.database import async_session
from sqlalchemy import select, update, and_
from datetime import datetime, timedelta

async def ensure_infinite_subscription():
    """Ensure @terentiev_v has infinite subscription"""
    async with async_session() as session:
        # Find user by username
        result = await session.execute(
            select(User).where(User.username == 'terentiev_v')
        )
        user = result.scalar_one_or_none()
        
        if user:
            print(f"✅ Found user: @{user.username}")
            
            # Check subscription
            result = await session.execute(
                select(Subscription).where(
                    and_(
                        Subscription.user_id == user.id,
                        Subscription.is_active == True
                    )
                )
            )
            subscription = result.scalar_one_or_none()
            
            now = datetime.utcnow()
            infinite_end_date = now + timedelta(days=365*100)  # 100 years
            
            if subscription:
                # Update to infinite if not already
                if subscription.plan_type != 'infinite' or subscription.end_date < infinite_end_date:
                    subscription.plan_type = 'infinite'
                    subscription.start_date = now
                    subscription.end_date = infinite_end_date
                    subscription.payment_method = 'admin_grant'
                    subscription.is_active = True
                    await session.commit()
                    print(f"✅ Updated to infinite subscription")
                else:
                    print(f"ℹ️ Already has infinite subscription")
            else:
                # Create infinite subscription
                subscription = Subscription(
                    user_id=user.id,
                    is_active=True,
                    plan_type='infinite',
                    start_date=now,
                    end_date=infinite_end_date,
                    payment_method='admin_grant',
                    transaction_id=f'admin_grant_{int(now.timestamp())}'
                )
                session.add(subscription)
                await session.commit()
                print(f"✅ Created infinite subscription")
        else:
            print(f"⚠️ User @terentiev_v not found in database")
            print("   Will be created on first /start command")

# Call this function in main.py startup