import asyncio
import aiofiles
import json

from bot.database.requests.client import get_enabled_clients, get_clients_address
from bot.database.models import Client
from bot.utils import conf, exec, generate_qrcode_bytes


class WireGuard:
    def __init__(self) -> None:
        self.__config_future = None

    async def gen_client_keys(self) -> dict:
        private_key = await exec('wg genkey')
        public_key = await exec(f'echo {private_key} | wg pubkey')
        preshare_key = await exec('wg genpsk')
        return {
            'private_key': private_key,
            'public_key': public_key,
            'preshare_key': preshare_key,
        }
    
    async def calc_next_client_ip(self) -> str | None:
        addresses = await get_clients_address()
        if not addresses:
            return conf.WG_DEFAULT_ADDRESS.replace('x', '2')
        
        addresses = set(map(lambda x: int(x.split('/')[0].split('.')[-1]), addresses))
        for i in range(2, 255): # 10.0.0.2/32 -> 10.0.0.254/32
            if i not in addresses:
                return conf.WG_DEFAULT_ADDRESS.replace('x', str(i))
        
        return None
    
    async def __build_config(self) -> dict:

        print('Loading configuration...')
        try:
            async with aiofiles.open(f'{conf.WG_PATH}/server_keys.json', 'r') as f:
                config = await f.read()
                config = json.loads(config)
            print('Configuration loaded.')

        except (FileNotFoundError, json.JSONDecodeError):
            print('Generating new configuration...')
            private_key = await exec('wg genkey')
            public_key = await exec(f'echo {private_key} | wg pubkey')
            address = conf.WG_DEFAULT_ADDRESS.replace('x', '1')
            config = {
                'private_key': private_key,
                'public_key': public_key,
                'address': address,
            }
            print('Configuration generated.')
            print('Saving new configuration...')
            async with aiofiles.open(f'{conf.WG_PATH}/server_keys.json', 'w+') as f:
                await f.write(json.dumps(config, indent=4))
            print('New configuration saved.')
        
        return config

    async def get_config(self) -> dict:
        if self.__config_future is None:
            self.__config_future = asyncio.ensure_future(self.__build_config())
        
        config = await self.__config_future
        await self.__save_config(config=config)
        # await exec('wg-quick down wg0')
        # await exec('wg-quick up wg0')
        await self.__sync_config()

        return config

    async def save_config(self) -> None:
        config = await self.get_config()
        await self.__save_config(config=config)
        await self.__sync_config()

    async def __save_config(self, config: dict) -> None:
        result = f"""# Server
[Interface]
PrivateKey = {config['private_key']}
Address = {config['address']}/24
ListenPort = {conf.WG_PORT}
PostUp = {conf.WG_POST_UP}
PostDown = {conf.WG_POST_DOWN}

"""
        clients = await get_enabled_clients()
        if clients:
            for client in clients:
                if not client.enabled:
                    continue

                result += f"""# Client {client.id}:{client.tg_id}:{client.name}
[Peer]
PublicKey = {client.public_key}
PresharedKey = {client.preshare_key}
AllowedIPs = {client.address}/32

"""
        async with aiofiles.open(f'{conf.WG_PATH}/wg0.conf', mode='w+') as file:
            await file.write(result)

    async def __sync_config(self) -> None:
        await exec('wg syncconf wg0 <(wg-quick strip wg0)')

    async def get_client_configuration(self, client: Client | None) -> str:
        config = await self.get_config()
        if client:
            return f"""# Configuration file for {client.tg_id}:{client.name}
[Interface]
PrivateKey = {client.private_key}
Address = {client.address}/32
DNS = {conf.WG_DEFAULT_DNS}

[Peer]
PublicKey = {config['public_key']}
PresharedKey = {client.preshare_key}
Endpoint = {conf.WG_HOST}:{conf.WG_PORT}
AllowedIPs = {conf.WG_ALLOWED_IPS}
PersistentKeepalive = {conf.WG_PERSISTENT_KEEPALIVE}
"""
        else:
            return ''
    
    async def get_client_qrcode_bytes(self, client: Client) -> bytes:
        config = await self.get_client_configuration(client=client)
        return generate_qrcode_bytes(data=config)
    
    async def start(self) -> None:
        await self.get_config()
        await exec('wg-quick up wg0')
        # await exec('systemctl enable wg-quick@wg0.service')
        # await exec('systemctl start wg-quick@wg0.service')

    async def stop(self) -> None:
        await exec('wg-quick down wg0')
        # await exec('systemctl stop wg-quick@wg0.service')
        # await exec('systemctl disable wg-quick@wg0.service')