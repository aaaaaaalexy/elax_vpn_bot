from aiogram import types

import bot.database.requests as rq
from bot.keyboards import after_connect_keyboard
from bot.misc.messages import after_connect_message
from bot.utils import get_default_time_sub


async def callback_connect_to_db(callback: types.CallbackQuery) -> None:
    await rq.set_user(tg_id=callback.from_user.id,
                      tg_firstname=callback.from_user.first_name,
                      time_sub=get_default_time_sub())
    await callback.answer('Вы успешно подключены к VPN!')
    await callback.message.edit_text(after_connect_message, reply_markup=after_connect_keyboard)
    await callback.answer()