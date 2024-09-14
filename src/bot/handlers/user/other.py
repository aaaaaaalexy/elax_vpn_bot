from aiogram import types

import bot.database.requests as rq
from bot.keyboards import main_keyboard
from bot.misc.messages import main_message


async def callback_home(callback: types.CallbackQuery) -> None:
    user = await rq.get_user(tg_id=callback.from_user.id)
    await callback.message.edit_text(main_message(user=user),
                                     reply_markup=main_keyboard,
                                     link_preview_options=types.LinkPreviewOptions(is_disabled=True,
                                                                                   show_above_text=False))
    await callback.answer()


async def callback_cancel(callback: types.CallbackQuery) -> None:
    await callback.answer('Действие отменено!')
    await callback_home(callback)