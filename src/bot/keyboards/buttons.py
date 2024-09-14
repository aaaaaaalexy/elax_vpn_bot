from bot.utils import ClientAction, ClientsCallbackFactory
from bot.utils import PaymentAction, PaymentsCallbackFactory


create_payment = '💰 Пополнить баланс'
payments_history = '🧾 История платежей'
to_pay = '💳 Оплатить'
check_payment = '✔️ Проверить оплату'


class Button:
    _connect_to_db = ('🔗 Подключиться к VPN', 'connect_to_db')
    _get_started = ('🚀 Начать работу', 'home')
    _home = ('🏠 Главное меню', 'home')
    _help = ('📋 Помощь и справка', 'help')
    _help_all = ('🛠️ Команды', 'help_all')
    _my_clients = ('💻 Мои устройства', 'my_clients')
    _balance = ('💵 Управление балансом', 'my_balance')
    _instruction = ('📕 Инструкция по подключению', 'instruction')
    _create_client = ('📝 Добавить', 'create_client')
    _delete_client = ('🗑️ Удалить', 'delete_client')
    _cancel = ('🚫 Отмена', 'cancel')
    _send_phone_number = '📞 Отправить'
    _client_about = lambda client: (
        f'🗝️ Устройство {client.name}',
        ClientsCallbackFactory(client_id=client.id,
                               action=ClientAction.about).pack()
    )
    _client_to_be_deleted = lambda client: (
        f'🗝️ Устройство {client.name}',
        ClientsCallbackFactory(client_id=client.id,
                               action=ClientAction.delete).pack()
    )
    _client_delete = lambda client: (
        f'🗑️ Удалить',
        ClientsCallbackFactory(client_id=client.id,
                               action=ClientAction.delete).pack()
    )
    _client_confirm = lambda callback_data: (
        f'✅ Подтвердить',
        ClientsCallbackFactory(client_id=callback_data.client_id,
                               action=callback_data.action,
                               confirm=True).pack()
    )
    _client_get_conf_file = lambda client: (
        f'📄 Файл',
        ClientsCallbackFactory(client_id=client.id,
                               action=ClientAction.get_conf_file).pack()
    )
    _client_get_qrcode = lambda client: (
        f'📷 QR-код',
        ClientsCallbackFactory(client_id=client.id,
                               action=ClientAction.get_qrcode).pack()
    )
    _payment_create_payment = lambda tg_id: (
        create_payment,
        PaymentsCallbackFactory(tg_id=tg_id,
                                action=PaymentAction.create_payment).pack()
    )
    _payment_to_pay = lambda tg_id: (
        to_pay,
        PaymentsCallbackFactory(tg_id=tg_id,
                                action=PaymentAction.to_pay).pack()
    )
    _payment_check_payment = lambda tg_id, payment_id: (
        check_payment,
        PaymentsCallbackFactory(tg_id=tg_id,
                                action=PaymentAction.check_payment,
                                payment_id=payment_id).pack()
    )
    _payment_history = lambda tg_id: (
        payments_history,
        PaymentsCallbackFactory(tg_id=tg_id,
                                action=PaymentAction.get_history).pack()
    )