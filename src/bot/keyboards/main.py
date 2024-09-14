from bot.keyboards.inline import *
from bot.keyboards import Button


start_keyboard = get_keyboard([
    [Button._connect_to_db],
])

after_connect_keyboard = get_keyboard([
    [Button._get_started],
])

main_keyboard = get_keyboard([
    [Button._my_clients],
    [Button._help_all, Button._help],
    [Button._balance],
])

def my_clients_keyboard(clients):
    if clients is None:
        return get_keyboard([
            [Button._create_client],
            [Button._home],
        ])
    else:
        return get_keyboard([
            *[[Button._client_about(client=client)] for client in clients],
            [Button._create_client, Button._delete_client],
            [Button._instruction],
            [Button._home],
        ])
    
delete_client_keyboard = lambda clients: get_keyboard([
    *[[Button._client_to_be_deleted(client=client)] for client in clients],
    [Button._cancel],
])

confirm_keyboard = lambda callback_data: get_keyboard([
    [Button._cancel, Button._client_confirm(callback_data=callback_data)],
])

about_client_keyboard = lambda client: get_keyboard([
    [Button._client_get_conf_file(client=client), Button._client_get_qrcode(client=client)],
    [Button._client_delete(client=client)],
    [Button._my_clients],
])

balance_keyboard = lambda tg_id: get_keyboard([
    [Button._payment_create_payment(tg_id=tg_id)],
    [Button._payment_history(tg_id=tg_id)],
    [Button._home]
])

request_contact_keyboard = get_contact_keyboard(Button._send_phone_number) 

payment_keyboard = lambda tg_id: get_keyboard([
    [Button._payment_create_payment(tg_id=tg_id)],
    [Button._payment_history(tg_id=tg_id)],
])

create_payment_keyboard = lambda tg_id, payment_url, payment_id: get_keyboard_with_urls([
    [(Button._payment_to_pay(tg_id=tg_id), payment_url)],
    [(Button._payment_check_payment(tg_id=tg_id, payment_id=payment_id), None)],
])

go_home_keyboard = get_keyboard([
    [Button._home],
])