from aiogram import Router
from aiogram.filters.command import Command
from aiogram import F

from bot.handlers.user.start import cmd_start
from bot.handlers.user.connect import callback_connect_to_db
from bot.utils import ClientAction, ClientsCallbackFactory
from bot.handlers.user.clients import (
    cmd_my_clients,
    callback_my_clients,
    callback_create_client, 
    callback_client_is_selected,
    callback_delete_client, callback_delete_selected_client,
)
from bot.handlers.user.other import callback_home, callback_cancel


def register_user_handlers(router: Router) -> None:
    router.message.register(cmd_start, Command('start'))
    router.callback_query.register(callback_home, F.data == 'home')
    router.callback_query.register(callback_cancel, F.data == 'cancel')

    router.callback_query.register(callback_connect_to_db, F.data == 'connect_to_db')

    router.message.register(cmd_my_clients, Command('devices'))
    router.callback_query.register(callback_my_clients, F.data == 'my_clients')
    router.callback_query.register(callback_create_client, F.data == 'create_client')
    router.callback_query.register(callback_delete_client, F.data == 'delete_client')
    router.callback_query.register(callback_delete_selected_client,
                                   ClientsCallbackFactory.filter(F.action == ClientAction.delete and F.confirm == True))
    router.callback_query.register(callback_client_is_selected, ClientsCallbackFactory.filter())
    
