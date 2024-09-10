from aiogram import Router

from bot.middlewares.time_sub import register_time_sub_middlewire
from bot.handlers import (
    common_router,
    user_router,
    payment_router,
)

def register_all_middlewires(router: Router) -> None:
    register_time_sub_middlewire(user_router)