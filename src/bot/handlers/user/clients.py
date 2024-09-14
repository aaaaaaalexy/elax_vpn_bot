from aiogram import types
from aiogram.types import BufferedInputFile

import bot.database.requests as rq
from bot.keyboards import (
    my_clients_keyboard,
    delete_client_keyboard, confirm_keyboard,
    about_client_keyboard,
    go_home_keyboard,
    start_keyboard,
)
from bot.misc.messages import (
    my_clients_message, no_clients_message,
    select_client_to_be_deleted_message, confirm_delete_message,
    about_client_message,
    get_conf_message, get_qrcode_message,
    instruction_message,
    not_registered_message,
)
from bot.utils import conf
from bot.utils import ClientAction, ClientsCallbackFactory
from bot.wireguard import wg


async def cmd_my_clients(message: types.Message) -> None:
    if await rq.user_is_registered(tg_id=message.from_user.id):
        clients = await rq.get_clients_by_tg_id(tg_id=message.from_user.id)
        if clients is None:
            await message.answer(no_clients_message,
                                reply_markup=my_clients_keyboard(clients=clients))
        else:
            await message.answer(my_clients_message,
                                reply_markup=my_clients_keyboard(clients=clients))
    else:
        await message.answer(not_registered_message,
                             reply_markup=start_keyboard)


async def callback_my_clients(callback: types.CallbackQuery) -> None:
    clients = await rq.get_clients_by_tg_id(tg_id=callback.from_user.id)
    if clients is None:
        await callback.message.edit_text(no_clients_message, 
                                         reply_markup=my_clients_keyboard(clients=clients))
    else:
        await callback.message.edit_text(my_clients_message, 
                                         reply_markup=my_clients_keyboard(clients=clients))
    await callback.answer()


async def cmd_instruction(message: types.Message) -> None:
    if await rq.user_is_registered(tg_id=message.from_user.id):
        await message.answer(instruction_message,
                            link_preview_options=types.LinkPreviewOptions(is_disabled=True,
                                                                        show_above_text=False))
    else:
        await message.answer(not_registered_message,
                             reply_markup=start_keyboard)
    

async def callback_instruction(callback: types.CallbackQuery) -> None:
    await callback.message.answer(instruction_message,
                                  reply_markup=go_home_keyboard,
                                  link_preview_options=types.LinkPreviewOptions(is_disabled=True,
                                                                                show_above_text=False))


async def callback_create_client(callback: types.CallbackQuery) -> None:
    clients = await rq.get_clients_by_tg_id(tg_id=callback.from_user.id)
    if clients:
        if len(clients) >= conf.MAX_CLIENT_COUNT:
            await callback.answer('Максимальное допустимое количество устройств!')
            return
    
    address = await wg.calc_next_client_ip()
    if address:
        keys = await wg.gen_client_keys()
        await rq.set_client(tg_id=callback.from_user.id,
                            address=address,
                            private_key=keys['private_key'],
                            public_key=keys['public_key'],
                            preshare_key=keys['preshare_key'])
        await wg.save_config()
        await callback.answer('Новое устройство добавлено!')
    else:
        await callback.answer('Ошибка при добавлении нового устройства\n\
                              (Достигнуто максимальное кол-во клиентов на сервере)')
    
    await callback_my_clients(callback)        


async def callback_delete_client(callback: types.CallbackQuery) -> None:
    clients = await rq.get_clients_by_tg_id(tg_id=callback.from_user.id)
    await callback.message.edit_text(select_client_to_be_deleted_message,
                                     reply_markup=delete_client_keyboard(clients=clients))
    await callback.answer()


async def callback_client_is_selected(callback: types.CallbackQuery,
                                      callback_data: ClientsCallbackFactory) -> None:
    client = await rq.get_client_by_id(id=callback_data.client_id)
    match callback_data.action:
        case ClientAction.about:
            await callback.message.edit_text(about_client_message(client=client),
                                             reply_markup=about_client_keyboard(client=client))
        case ClientAction.delete:
            await callback.message.edit_text(confirm_delete_message(client_name=client.name),
                                             reply_markup=confirm_keyboard(callback_data=callback_data))
        case ClientAction.get_conf_file:
            config = await wg.get_client_configuration(client=client)
            conf_file = BufferedInputFile(bytes(config, 'utf-8'), filename=f'{client.name}.conf')
            await callback.message.answer_document(document=conf_file,
                                                   caption=get_conf_message)
        case ClientAction.get_qrcode:
            qrcode = await wg.get_client_qrcode_bytes(client=client)
            qr_img = BufferedInputFile(qrcode, filename=f'{client.name}.png')
            await callback.message.answer_photo(photo=qr_img,
                                                caption=get_qrcode_message)

    await callback.answer()


async def callback_delete_selected_client(callback: types.CallbackQuery,
                                          callback_data: ClientsCallbackFactory) -> None:
    if callback_data.action == ClientAction.delete:
        if callback_data.confirm:
            await rq.delete_client(id=callback_data.client_id)
            await wg.save_config()
            await callback.answer(f'Устройство удалено!')
            await callback_my_clients(callback)