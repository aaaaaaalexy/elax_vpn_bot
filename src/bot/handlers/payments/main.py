from aiogram import Router
from aiogram.filters.command import Command
from aiogram import F

from bot.handlers.payments.payment import (
    cmd_balance, callback_balance,
    get_contact,
    callback_create_payment, callback_check_payment,
    callback_get_history,
)
from bot.utils import PaymentAction, PaymentsCallbackFactory


def register_payments_handlers(router: Router) -> None:
    router.message.register(cmd_balance, Command('balance'))

    router.callback_query.register(callback_balance, F.data == 'my_balance')

    router.message.register(get_contact, F.contact)

    router.callback_query.register(callback_create_payment,
                                   PaymentsCallbackFactory.filter(F.action == PaymentAction.create_payment))
    
    router.callback_query.register(callback_check_payment,
                                   PaymentsCallbackFactory.filter(F.action == PaymentAction.check_payment))
    
    router.callback_query.register(callback_get_history,
                                   PaymentsCallbackFactory.filter(F.action == PaymentAction.get_history))
    
