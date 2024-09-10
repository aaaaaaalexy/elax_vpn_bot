from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import bot.database.requests as rq
from bot.misc.messages import payment_now_not_enough_message
from bot.keyboards import payment_keyboard


class TimeSubMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        
        tg_id = data['event_from_user'].id

        if not await rq.user_is_registered(tg_id=tg_id):
            result = await handler(event, data)
            return result
        
        elif await rq.is_enabled(tg_id=tg_id):
            result = await handler(event, data)
            return result
        
        else:
            bot = data['bot']
            user = await rq.get_user(tg_id=tg_id)
            await bot.send_message(tg_id, 
                                   payment_now_not_enough_message(balance=user.balance),
                                   reply_markup=payment_keyboard(tg_id=tg_id))