import uuid

from yookassa import Configuration, Payment

from bot.utils import conf


def init_yookassa() -> None:
    Configuration.account_id = conf.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = conf.YOOKASSA_SECRET_KEY


async def create_payment(order_id: int, phone: str, autopay: bool = False) -> tuple[str, str]:
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        'amount': {
            'value': conf.SUB_PRICE,
            'currency': 'RUB',
        },
        'description': f'Оплата elaxvpn (№{order_id})',
        'receipt': {
            'customer': {
                'phone': phone,
            },
            'items': [
                {
                    'description': 'Пополнение баланса elaxvpn (1 мес.)',
                    'amount': {
                        'value': conf.SUB_PRICE,
                        'currency': 'RUB',
                    },
                    'vat_code': '1',
                    'quantity': '1',
                },
            ],
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/elaxvpn_bot',
        },
        # 'save_payment_method': autopay,
        # 'payment_method_id': '...',
        'capture': True,

    }, idempotence_key)

    return payment.confirmation.confirmation_url, payment.id


def get_payment_id(payment_id: str) -> str | bool:
    payment = Payment.find_one(payment_id=payment_id)
    if payment.status == 'succeeded':
        return payment.id
    else:
        return False