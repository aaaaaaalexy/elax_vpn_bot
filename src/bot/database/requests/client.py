from typing import Optional

from sqlalchemy import select, update

from bot.database.models import async_session
from bot.database.models import User, Client
from bot.utils import conf, generate_client_name
from bot.utils import debug


async def get_client_by_id(id: int) -> Client:
    async with async_session() as session:
        client = await session.scalar(select(Client).where(Client.id == id))
        return client


async def get_clients_by_tg_id(tg_id: int) -> list[Client]:
    async with async_session() as session:
        result = await session.scalars(select(Client).where(Client.tg_id == tg_id))
        clients = result.all()
        return clients if clients else None
    

async def get_enabled_clients() -> list[Client]:
    async with async_session() as session:
        result = await session.scalars(select(Client).where(Client.enabled == True))
        clients = result.all()
        return clients if clients else None
    

async def get_client_name(tg_id: int) -> str:
    clients = await get_clients_by_tg_id(tg_id=tg_id)
    if clients:
        names = [client.name for client in clients]
        new_name = generate_client_name()
        while new_name in names:
            new_name = generate_client_name()
        return new_name        
    else:
        return generate_client_name()
    

async def get_clients_address() -> list[str]:
    async with async_session() as session:
        result = await session.scalars(select(Client.address))
        adresses = result.all()
        return adresses if adresses else None


async def set_client(tg_id: int,
                     address: str,
                     private_key: str,
                     public_key: str,
                     preshare_key: str,
                     name: Optional[str] = None,
                     enabled: bool = conf.DEFAULT_CLIENT_ENABLED) -> None:
        async with async_session() as session:
            if name is None:
                name = await get_client_name(tg_id=tg_id)
            client = Client(
                tg_id=tg_id,
                name=name,
                address=address,
                private_key=private_key,
                public_key=public_key,
                preshare_key=preshare_key,
                enabled=enabled,
            )
            session.add(client)
            debug(f'Client {name} added.')
            await session.execute(
                update(User)
                .where(User.tg_id == tg_id)
                .values(count_clients=User.count_clients + 1)
            )
            await session.commit()


async def disable_clients_by_tg_id(tg_id: int) -> None:
    async with async_session() as session:
        clients = await get_clients_by_tg_id(tg_id=tg_id)
        if clients:
            for client in clients:
                client.enabled = False
                session.add(client)        
        debug(f'User {tg_id} all devices are disabled.')
        await session.commit()


async def enable_clients_by_tg_id(tg_id: int) -> None:
    async with async_session() as session:
        clients = await get_clients_by_tg_id(tg_id=tg_id)
        if clients:
            for client in clients:
                client.enabled = True
                session.add(client)
            debug(f'User {tg_id} all devices are enabled.')
            await session.commit()


async def delete_client(id: int) -> None:
    async with async_session() as session:
        client = await get_client_by_id(id=id)
        tg_id = client.tg_id
        client_name = client.name
        await session.delete(client)
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(count_clients=User.count_clients - 1)
        )
        debug(f'Client {client_name} deleted.')
        await session.commit()