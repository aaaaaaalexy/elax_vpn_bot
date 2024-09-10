from sqlalchemy import select

from bot.database.models import async_session
from bot.database.models import Payment
from bot.database.requests.user import get_user, is_enabled, change_balance, sub_payment
from bot.database.requests.client import enable_clients_by_tg_id
from bot.wireguard import wg


async def get_payment(id: int) -> Payment:
    async with async_session() as session:
        payment = await session.scalar(select(Payment).where(Payment.id == id))
        return payment
    

async def get_last_id() -> int:
    async with async_session() as session:
        result = await session.scalars(select(Payment).order_by(Payment.id.desc()))
        last_payment = result.first()
        return last_payment.id if last_payment else 0
    

async def get_history(tg_id: int) -> dict:
    async with async_session() as session:
        result = await session.scalars(select(Payment).where(Payment.tg_id == tg_id))
        payments = result.all()
        if payments:
            return {'column_names': ['DATE', 'BEFORE', 'SHIFT'],
                    'history': [
                        {
                            'created_at': str(payment.created_at).split('.')[0],
                            'balance_before': payment.balance_before,
                            'deposited': payment.deposited,
                        } for payment in payments]
                    }
        else:
            return {'column_names': ['DATE', 'BEFORE', 'SHIFT'],
                    'history': []}



async def set_payment(tg_id: int,
                      balance_before: int,
                      deposited: int,
                      uuid: str = None) -> None:
    async with async_session() as session:
        payment = Payment(
            tg_id=tg_id,
            balance_before=balance_before,
            deposited=deposited,
            uuid=uuid,
        )
        session.add(payment)
        await session.commit()


async def top_up_balance(tg_id: int, deposited: int, uuid: str) -> None:
    user = await get_user(tg_id=tg_id)
    balance_before = user.balance
    await set_payment(tg_id=tg_id,
                      balance_before=balance_before,
                      deposited=deposited,
                      uuid=uuid)
    await change_balance(tg_id=tg_id, shift=deposited)
    if not await is_enabled(tg_id=tg_id):
        await sub_payment(tg_id=tg_id)
        await enable_clients_by_tg_id(tg_id=tg_id)
        await wg.save_config()