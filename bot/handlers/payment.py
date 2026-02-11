from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import LabeledPrice, PreCheckoutQuery, ContentType
from bot.keyboards.main_menu import get_payment_method_menu, get_subscription_menu, get_stars_payment_keyboard
from bot.utils.localization import get_text
from bot.services.payment_service import PaymentService
from bot.database import async_session
from sqlalchemy import select, and_
from datetime import datetime, timedelta
import asyncio

class PaymentStates(StatesGroup):
    choosing_payment_method = State()
    waiting_crypto_payment = State()
    processing_stars_payment = State()

async def handle_payment_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора плана подписки"""
    lang = callback.from_user.language_code or 'en'
    plan_data = callback.data.replace('sub_', '')
    
    # Определяем план
    plans = {
        '1_month': {
            'price_usd': 0.99, 
            'price_stars': 99,
            'days': 30, 
            'name': '1 месяц'
        },
        '3_months': {
            'price_usd': 2.50, 
            'price_stars': 250,
            'days': 90, 
            'name': '3 месяца'
        },
        '6_months': {
            'price_usd': 5.00, 
            'price_stars': 500,
            'days': 180, 
            'name': '6 месяцев'
        },
        '12_months': {
            'price_usd': 10.00, 
            'price_stars': 1000,
            'days': 365, 
            'name': '12 месяцев'
        }
    }
    
    if plan_data not in plans:
        await callback.answer("Неверный план")
        return
    
    plan = plans[plan_data]
    await state.update_data(plan_type=plan_data, plan=plan)
    
    # Проверяем, нет ли уже активной подписки
    async with async_session() as session:
        result = await session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == callback.from_user.id,
                    Subscription.is_active == True,
                    Subscription.end_date > datetime.now()
                )
            )
        )
        existing_sub = result.scalar_one_or_none()
        
        if existing_sub:
            # Предлагаем продлить существующую подписку
            new_end_date = existing_sub.end_date + timedelta(days=plan['days'])
            await state.update_data(extend_existing=True, existing_end_date=existing_sub.end_date)
            
            text = f"У вас уже есть активная подписка до {existing_sub.end_date.strftime('%d.%m.%Y')}\n"
            text += f"Добавить {plan['name']}?\n"
            text += f"💰 Стоимость: ${plan['price_usd']} или {plan['price_stars']} ⭐\n"
            text += f"📅 Новая дата окончания: {new_end_date.strftime('%d.%m.%Y')}\n\n"
            text += "Выберите способ оплаты:"
        else:
            text = f"Вы выбрали: {plan['name']}\n"
            text += f"💰 Стоимость: ${plan['price_usd']} или {plan['price_stars']} ⭐\n"
            text += f"📅 Срок действия: {plan['days']} дней\n\n"
            text += "Выберите способ оплаты:"
    
    await PaymentStates.choosing_payment_method.set()
    await callback.message.edit_text(
        text, 
        reply_markup=get_payment_method_menu(lang, plan_data)
    )

async def handle_payment_method(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора способа оплаты"""
    lang = callback.from_user.language_code or 'en'
    data_parts = callback.data.split(':')
    method = data_parts[0].replace('pay_', '')
    plan_type = data_parts[1] if len(data_parts) > 1 else None
    
    if not plan_type:
        # Получаем plan_type из state
        state_data = await state.get_data()
        plan_type = state_data.get('plan_type')
    
    data = await state.get_data()
    plan = data.get('plan')
    
    if not plan:
        # Если план не найден в state, создаем его из plan_type
        plans = {
            '1_month': {'price_usd': 0.99, 'price_stars': 99, 'days': 30, 'name': '1 месяц'},
            '3_months': {'price_usd': 2.50, 'price_stars': 250, 'days': 90, 'name': '3 месяца'},
            '6_months': {'price_usd': 5.00, 'price_stars': 500, 'days': 180, 'name': '6 месяцев'},
            '12_months': {'price_usd': 10.00, 'price_stars': 1000, 'days': 365, 'name': '12 месяцев'}
        }
        plan = plans.get(plan_type)
    
    payment_service = PaymentService()
    
    if method == 'crypto':
        # Генерируем адрес для оплаты криптовалютой
        payment_data = await payment_service.process_crypto_payment(
            user_id=callback.from_user.id,
            amount=plan['price_usd'],
            plan_type=plan_type
        )
        
        text = f"💳 <b>Оплата криптовалютой</b>\n\n"
        text += f"💰 Сумма: ${plan['price_usd']}\n"
        text += f"🏦 Адрес: <code>{payment_data['crypto_address']}</code>\n\n"
        text += "📤 Отправьте указанную сумму на указанный адрес.\n"
        text += "⏳ После получения платежа подписка будет активирована автоматически.\n\n"
        text += "⚠️ Проверка платежа занимает до 15 минут."
        
        # Сохраняем данные о платеже
        await state.update_data(
            payment_method='crypto',
            transaction_id=payment_data['transaction_id'],
            crypto_address=payment_data['crypto_address'],
            plan_type=plan_type
        )
        
        await PaymentStates.waiting_crypto_payment.set()
        await callback.message.edit_text(text, parse_mode='HTML')
        
        # Запускаем проверку платежа в фоне
        asyncio.create_task(check_crypto_payment(callback, state))
        
    elif method == 'stars':
        # Telegram Stars оплата
        text = f"⭐ <b>Оплата Telegram Stars</b>\n\n"
        text += f"💰 Стоимость: {plan['price_stars']} Stars (${plan['price_usd']})\n"
        text += f"📅 План: {plan['name']}\n\n"
        text += "💳 Для оплаты используйте кнопку ниже:"
        
        # Создаем инвойс
        invoice = payment_service.create_stars_invoice(plan_type, callback.from_user.id)
        
        try:
            # Отправляем инвойс
            await callback.bot.send_invoice(
                chat_id=callback.from_user.id,
                title=invoice['title'],
                description=invoice['description'],
                payload=invoice['payload'],
                provider_token=invoice['provider_token'],
                currency=invoice['currency'],
                prices=invoice['prices'],
                start_parameter=invoice['start_parameter'],
                need_email=invoice['need_email'],
                need_phone_number=invoice['need_phone_number'],
                need_shipping_address=invoice['need_shipping_address'],
                is_flexible=invoice['is_flexible']
            )
            
            # Сохраняем данные
            await state.update_data(
                payment_method='stars',
                plan_type=plan_type,
                stars_amount=plan['price_stars'],
                invoice_payload=invoice['payload']
            )
            
            await PaymentStates.processing_stars_payment.set()
            
            # Удаляем предыдущее сообщение
            await callback.message.delete()
            
        except Exception as e:
            error_text = f"❌ Ошибка при создании платежа: {str(e)}"
            await callback.message.edit_text(error_text)

async def check_crypto_payment(callback: types.CallbackQuery, state: FSMContext):
    """Проверка криптоплатежа"""
    data = await state.get_data()
    transaction_id = data.get('transaction_id')
    payment_service = PaymentService()
    
    # Проверяем платеж каждые 30 секунд в течение 10 минут
    for _ in range(20):
        await asyncio.sleep(30)
        
        status = await payment_service.check_payment_status(transaction_id)
        
        if status.get('status') == 'completed':
            # Активируем подписку
            await activate_subscription(
                user_id=callback.from_user.id,
                plan_type=data['plan_type'],
                payment_method='crypto',
                transaction_id=transaction_id
            )
            
            lang = callback.from_user.language_code or 'en'
            text = get_text('success.payment_received', lang)
            
            # Отправляем сообщение
            await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=text
            )
            
            await state.finish()
            return
    
    # Если платеж не подтвердился
    lang = callback.from_user.language_code or 'en'
    text = get_text('errors.payment_timeout', lang)
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=text
    )
    await state.finish()

async def activate_subscription(user_id: int, plan_type: str, payment_method: str, transaction_id: str):
    """Активация подписки"""
    async with async_session() as session:
        from bot.database import User, Subscription, Payment
        
        # Проверяем существующую подписку
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        subscription = result.scalar_one_or_none()
        
        # Определяем длительность
        from bot.config import config
        duration_days = config.SUBSCRIPTION_DURATIONS.get(plan_type, 30)
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        
        if subscription:
            # Продлеваем существующую подписку
            if subscription.end_date and subscription.end_date > start_date:
                end_date = subscription.end_date + timedelta(days=duration_days)
            
            subscription.is_active = True
            subscription.plan_type = plan_type
            subscription.start_date = start_date
            subscription.end_date = end_date
            subscription.payment_method = payment_method
            subscription.transaction_id = transaction_id
        else:
            # Создаем новую подписку
            subscription = Subscription(
                user_id=user_id,
                is_active=True,
                plan_type=plan_type,
                start_date=start_date,
                end_date=end_date,
                payment_method=payment_method,
                transaction_id=transaction_id
            )
            session.add(subscription)
        
        # Создаем запись о платеже
        payment = Payment(
            user_id=user_id,
            amount=float(transaction_id.split('_')[-1]) if '_' in transaction_id else 0,
            currency='USD' if payment_method == 'crypto' else 'XTR',
            plan_type=plan_type,
            status='completed',
            transaction_id=transaction_id,
            payment_method=payment_method,
            created_at=start_date,
            confirmed_at=datetime.now()
        )
        session.add(payment)
        
        await session.commit()

# Обработчики для Telegram Stars платежей
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    """Обработка предварительного запроса на оплату"""
    # Можно проверить данные перед оплатой
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True
    )

async def successful_payment_handler(message: types.Message, state: FSMContext):
    """Обработка успешной оплаты Telegram Stars"""
    payment_info = message.successful_payment
    
    # Извлекаем данные из payload
    payload_parts = payment_info.invoice_payload.split(':')
    
    if len(payload_parts) >= 3 and payload_parts[0] == 'subscription':
        plan_type = payload_parts[1]
        user_id = int(payload_parts[2])
        
        # Проверяем, что платеж соответствует текущему пользователю
        if user_id != message.from_user.id:
            await message.answer("❌ Ошибка: неверный пользователь")
            return
        
        # Создаем транзакцию
        transaction_id = f"stars_{user_id}_{int(datetime.now().timestamp())}"
        
        # Активируем подписку
        await activate_subscription(
            user_id=user_id,
            plan_type=plan_type,
            payment_method='stars',
            transaction_id=transaction_id
        )
        
        # Получаем язык пользователя
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = result.scalar_one_or_none()
            lang = user.language if user else 'en'
        
        # Отправляем подтверждение
        text = get_text('success.payment_received', lang)
        text += f"\n\n💎 План: {plan_type.replace('_', ' ')}"
        text += f"\n💰 Оплачено: {payment_info.total_amount / 100} Stars"
        text += f"\n📅 Подписка активирована!"
        
        await message.answer(text)
        
        # Завершаем состояние
        await state.finish()

def register_payment_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков платежей"""
    dp.register_callback_query_handler(handle_payment_callback, lambda c: c.data.startswith('sub_'))
    dp.register_callback_query_handler(handle_payment_method, lambda c: c.data.startswith('pay_'), state=PaymentStates.choosing_payment_method)
    
    # Регистрируем обработчики для Telegram Stars
    dp.register_pre_checkout_query_handler(pre_checkout_query_handler)
    dp.register_message_handler(successful_payment_handler, content_types=ContentType.SUCCESSFUL_PAYMENT)