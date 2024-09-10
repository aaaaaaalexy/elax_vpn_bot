from aiogram import Router
from aiogram.filters.command import Command
from aiogram import F

from bot.handlers.common.help import cmd_help, callback_help, callback_help_all


def register_common_handlers(router: Router) -> None:

    router.message.register(cmd_help, Command('help'))
    router.callback_query.register(callback_help, F.data == 'help')
    router.callback_query.register(callback_help_all, F.data == 'help_all')
