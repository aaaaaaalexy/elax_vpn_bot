import asyncio
import random, string
from enum import Enum
import qrcode, io
from datetime import date, timedelta
from typing import Optional

from aiogram.filters.callback_data import CallbackData

from .config import conf


class ClientAction(str, Enum):
    about = 'about'
    delete = 'delete'
    get_conf_file = 'get_conf_file'
    get_qrcode = 'get_qrcode'


class PaymentAction(str, Enum):
    create_payment = 'create'
    to_pay = 'to_pay'
    check_payment = 'check'
    get_history = 'get_history'


class ClientsCallbackFactory(CallbackData, prefix='client'):
    client_id: int
    action: ClientAction
    confirm: Optional[bool] = None


class PaymentsCallbackFactory(CallbackData, prefix='payment'):
    tg_id: int
    action: PaymentAction
    payment_id: Optional[str] = None


def generate_client_name() -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def get_default_time_sub() -> date:
    return date.today() + timedelta(days=conf.DEFAULT_TIME_SUB)


def plural_days(n: int) -> str:
    days = ['день', 'дня', 'дней']
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]


def generate_qrcode_bytes(data: str) -> bytes:
    buf = io.BytesIO()
    qr = qrcode.QRCode(
        version=12,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image()
    img.save(buf)
    buf.seek(0)
    return buf.read()


def dict_to_table(dict: dict) -> dict:
    """
    Only for dictionaries like below.
    {
        'column_names': [],
        'history': [
            {
                'created_at': payment.created_at,
                'balance_before': payment.balance_before,
                'deposited': payment.deposited,
            } for payment in payments]
    }
    """
    result = ''
    column_names: list = dict['column_names']
    history: list = dict['history']
    result += '{:<19} {:<10} {:<10}'.format(*column_names)
    result += '\n'
    if len(history) > 10:
        for log in history[:5]:
            result += '{:<19} {:<10} {:<10}\n'.format(*list(log.values()))
        result += '...\n'
        for log in history[-5:]:
            result += '{:<19} {:<10} {:<10}\n'.format(*list(log.values()))
    else:
        for log in history:
            result += '{:<19} {:<10} {:<10}\n'.format(*list(log.values()))
    result += '\n'

    return str(result)


async def exec(cmd: str) -> str:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()
        
        if stderr:
            return stderr.decode()[:-1]
        if stdout:
            return stdout.decode()[:-1]