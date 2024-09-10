from aiogram import Router

from .time_sub import TimeSubMiddleware

def register_time_sub_middlewire(router: Router) -> None:
    router.callback_query.middleware(TimeSubMiddleware())
    router.message.middleware(TimeSubMiddleware())