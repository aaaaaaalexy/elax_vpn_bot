from aiogram import types

import bot.database.requests as rq
from bot.utils import PaymentAction, PaymentsCallbackFactory, conf
from bot.misc.messages import (
    request_contact_message, we_get_your_phone_message,
    create_payment_message, 
    failed_payment_message, succeeded_payment_message,
    balance_message,
    payments_history_message,
)
from bot.keyboards import (
    balance_keyboard, payment_keyboard,
    request_contact_keyboard,
    create_payment_keyboard, go_home_keyboard,
)
from bot.payments import create_payment, get_payment_id


async def cmd_balance(message: types.Message) -> None:
    user = await rq.get_user(tg_id=message.from_user.id)
    await message.answer(balance_message(balance=user.balance),
                         reply_markup=payment_keyboard(tg_id=message.from_user.id))


async def callback_balance(callback: types.CallbackQuery) -> None:
    user = await rq.get_user(tg_id=callback.from_user.id)
    await callback.message.edit_text(balance_message(balance=user.balance),
                                     reply_markup=balance_keyboard(tg_id=callback.from_user.id))
    await callback.answer()


async def callback_get_history(callback: types.CallbackQuery,
                                 callback_data: PaymentsCallbackFactory) -> None:
    if callback_data.action == PaymentAction.get_history:
        history = await rq.get_history(tg_id=callback_data.tg_id)
        await callback.message.answer(payments_history_message(history=history),
                                      reply_markup=go_home_keyboard)


async def get_contact(message: types.Message) -> None:
    if message.contact:
        contact = message.contact.phone_number.replace('+', '')
        await rq.update_contact(tg_id=message.from_user.id, contact=contact)
        await message.answer(we_get_your_phone_message, reply_markup=types.ReplyKeyboardRemove())
        order_id = await rq.get_last_id()
        order_id += 1
        payment_url, payment_id = await create_payment(order_id=order_id,
                                                       phone=contact)
        await message.answer(create_payment_message,
                             reply_markup=create_payment_keyboard(tg_id=message.from_user.id,
                                                                  payment_url=payment_url,
                                                                  payment_id=payment_id))


async def callback_create_payment(callback: types.CallbackQuery,
                                  callback_data: PaymentsCallbackFactory) -> None:
    if callback_data.action == PaymentAction.create_payment:
        user = await rq.get_user(tg_id=callback_data.tg_id)
        if user.contact:
            order_id = await rq.get_last_id()
            order_id += 1
            payment_url, payment_id = await create_payment(order_id=order_id,
                                                        phone=user.contact)
            await callback.message.answer(create_payment_message,
                                          reply_markup=create_payment_keyboard(tg_id=user.tg_id,
                                                                               payment_url=payment_url,
                                                                               payment_id=payment_id))
        else:
            await callback.message.answer(request_contact_message,
                                          reply_markup=request_contact_keyboard)
            


async def callback_check_payment(callback: types.CallbackQuery,
                                 callback_data: PaymentsCallbackFactory) -> None:
    if callback_data.action == PaymentAction.check_payment:
        payment_id = get_payment_id(payment_id=callback_data.payment_id)
        if payment_id:
            await rq.top_up_balance(tg_id=callback_data.tg_id, deposited=conf.SUB_PRICE, uuid=payment_id)
            await callback.message.edit_text(succeeded_payment_message,
                                             reply_markup=go_home_keyboard)
        else:
            await callback.message.edit_text(failed_payment_message,
                                             reply_markup=callback.message.reply_markup)