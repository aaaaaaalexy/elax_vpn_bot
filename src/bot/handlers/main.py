from aiogram import Router
from aiogram import types

from bot.handlers.common import register_common_handlers
from bot.handlers.user import register_user_handlers
from bot.handlers.payments import register_payments_handlers
from bot.utils import debug


common_router = Router()
user_router = Router()
payment_router = Router()


async def error_handler(event: types.ErrorEvent):
    debug(str(event.exception))


def register_all_handlers(router: Router) -> None:
    register_common_handlers(common_router)
    register_user_handlers(user_router)
    register_payments_handlers(payment_router)

    router.include_routers(payment_router, common_router, user_router)

    router.error.register(error_handler)
    payment_router.error.register(error_handler)
    common_router.error.register(error_handler)
    user_router.error.register(error_handler)