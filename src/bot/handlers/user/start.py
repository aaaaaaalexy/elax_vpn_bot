from aiogram import types

import bot.database.requests as rq
from bot.keyboards import start_keyboard, main_keyboard
from bot.misc.messages import *


async def cmd_start(message: types.Message) -> None:
    is_registered = await rq.user_is_registered(tg_id=message.from_user.id)
    if not is_registered:
        await message.answer(hello_message(firstname=message.from_user.first_name),
                             reply_markup=start_keyboard)
    else:
        user = await rq.get_user(tg_id=message.from_user.id)
        await message.answer(main_message(user=user),
                             reply_markup=main_keyboard,
                             link_preview_options=types.LinkPreviewOptions(is_disabled=True,
                                                                           show_above_text=False))
