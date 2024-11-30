from datetime import date, timedelta

from aiogram import Bot
from sqlalchemy import select

from bot.database.models import async_session
from bot.database.models import User, Payment
from bot.database.requests.client import disable_clients_by_tg_id
from bot.misc.messages import (
    payment_tomorrow_good_message, payment_tomorrow_not_enough_message,
    payment_now_good_message, payment_now_not_enough_message,
)
from bot.keyboards import payment_keyboard
from bot.utils import conf
from bot.utils import debug
from bot.wireguard import wg


async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def set_user(tg_id: int,
                   tg_firstname: str,
                   time_sub: date,
                   contact: str = None,
                   balance: int = conf.DEFAULT_BALANCE,
                   enabled: bool = conf.DEFAULT_USER_ENABLED,
                   count_clients: int = conf.DEFAULT_COUNT_CLIENTS) -> None:
    async with async_session() as session:
        user = User(
            tg_id=tg_id,
            tg_firstname=tg_firstname,
            contact=contact,
            balance=balance,
            time_sub=time_sub,
            enabled=enabled,
            count_clients=count_clients,
        )
        session.add(user)
        debug(f'User {tg_id} added.')
        # if count_clients > 0:
        # ...
        await session.commit()


async def user_is_registered(tg_id: int) -> bool:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result is not None


async def is_enabled(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.enabled
    

async def update_contact(tg_id: int, contact: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.contact = contact
        session.add(user)
        debug(f'User {tg_id} updated contact.')
        await session.commit()


async def change_balance(tg_id: int, shift: int) -> None:
    async with async_session() as session:
        user = await get_user(tg_id=tg_id)
        user.balance += shift
        session.add(user)
        debug(f'User {tg_id} changed balance to {shift}.')
        await session.commit()


async def sub_payment(tg_id: int) -> None:
    async with async_session() as session:
        user = await get_user(tg_id=tg_id)
        if user.balance >= conf.SUB_PRICE:
            balance_before = user.balance
            user.balance -= conf.SUB_PRICE
            user.time_sub += timedelta(days=conf.TIME_SUB)
            user.enabled = True
            user.reminder_sent = [False, False]
            payment = Payment(
                tg_id=tg_id,
                balance_before=balance_before,
                deposited=-conf.SUB_PRICE,
            )
            session.add(payment)
            debug(f'User {tg_id} successfully paid for the sub until {user.time_sub} (balance: {user.balance}).')
        else:
            user.enabled = False
            debug(f'User {tg_id} is disabled because not enough funds on balance ({user.balance}).')
        session.add(user)
        await session.commit()


async def check_subscriptions(bot: Bot):
    async with async_session() as session:
        today = date.today()
        reminder_interval = 1
        
        result = await session.scalars(select(User).where(User.enabled == True))
        users = result.all()
        
        for user in users:
            try:
                days_left = (user.time_sub - today).days
                
                if not user.reminder_sent[0]:
                    if days_left == reminder_interval:
                        if user.balance >= conf.SUB_PRICE:
                            await bot.send_message(user.tg_id, 
                                                payment_tomorrow_good_message(balance=user.balance),
                                                reply_markup=payment_keyboard(tg_id=user.tg_id))
                        else:
                            await bot.send_message(user.tg_id, 
                                                payment_tomorrow_not_enough_message(balance=user.balance),
                                                reply_markup=payment_keyboard(tg_id=user.tg_id))
                        user.reminder_sent = [True, user.reminder_sent[1]]
                        session.add(user)
                        debug(f'User {user.tg_id} notified about debiting tomorrow.')
                
                elif not user.reminder_sent[1]:
                    if days_left <= 0:
                        if user.balance >= conf.SUB_PRICE:
                            balance_before = user.balance
                            user.balance -= conf.SUB_PRICE
                            user.time_sub += timedelta(days=conf.TIME_SUB)
                            user.enabled = True
                            user.reminder_sent = [False, False]
                            payment = Payment(
                                tg_id=user.tg_id,
                                balance_before=balance_before,
                                deposited=-conf.SUB_PRICE,
                            )
                            session.add(payment)
                            await bot.send_message(user.tg_id, 
                                                payment_now_good_message(balance=user.balance),
                                                reply_markup=payment_keyboard(tg_id=user.tg_id))
                            debug(f'User {user.tg_id} notified about debiting funds.')
                        else:
                            user.enabled = False
                            user.reminder_sent = [user.reminder_sent[0], True]
                            await disable_clients_by_tg_id(tg_id=user.tg_id)
                            await wg.save_config()
                            await bot.send_message(user.tg_id, 
                                                payment_now_not_enough_message(balance=user.balance),
                                                reply_markup=payment_keyboard(tg_id=user.tg_id))
                            debug(f'User {user.tg_id} notified of shutdown.')
                        session.add(user)
            except Exception as e:
                debug(str(e))
        
        await session.commit()
