import os
from dotenv import load_dotenv, find_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.BOT_TOKEN: str = self.get_str('BOT_TOKEN')

        self.SQLALCHEMY_URL: str = self.get_sqalchemy_url()

        self.SUB_PRICE: int = self.get_int('SUB_PRICE')
        self.DEFAULT_BALANCE: int = self.get_int('DEFAULT_BALANCE')
        self.TIME_SUB: int = self.get_int('TIME_SUB')
        self.DEFAULT_TIME_SUB: int = self.get_int('DEFAULT_TIME_SUB')
        self.DEFAULT_COUNT_CLIENTS: int = self.get_int('DEFAULT_COUNT_CLIENTS')
        self.DEFAULT_USER_ENABLED: bool = self.get_bool('DEFAULT_USER_ENABLED')
        self.DEFAULT_CLIENT_ENABLED: bool = self.get_bool('DEFAULT_CLIENT_ENABLED')
        self.MAX_CLIENT_COUNT: int = self.get_int('MAX_CLIENT_COUNT')

        self.WG_PATH: str = self.get_str('WG_PATH')
        self.WG_DEVICE: str = self.get_str('WG_DEVICE')
        self.WG_HOST: str = self.get_str('WG_HOST')
        self.WG_PORT: str = self.get_str('WG_PORT')
        self.WG_DEFAULT_DNS: str = self.get_str('WG_DEFAULT_DNS')
        self.WG_DEFAULT_ADDRESS: str = self.get_str('WG_DEFAULT_ADDRESS')
        self.WG_PERSISTENT_KEEPALIVE: int = self.get_int('WG_PERSISTENT_KEEPALIVE')
        self.WG_ALLOWED_IPS: str = self.get_str('WG_ALLOWED_IPS')
        self.WG_POST_UP: str  = self.get_wg_post_cmd('WG_POST_UP')
        self.WG_POST_DOWN: str = self.get_wg_post_cmd('WG_POST_DOWN')

        self.YOOKASSA_ACCOUNT_ID: str = self.get_str('YOOKASSA_ACCOUNT_ID')
        self.YOOKASSA_SECRET_KEY: str = self.get_str('YOOKASSA_SECRET_KEY')

    def get_str(self, var: str) -> str:
        return os.getenv(var)

    def get_int(self, var: str) -> int:
        return int(os.getenv(var))
    
    def get_bool(self, var: str) -> bool:
        return os.getenv(var).lower() in ('true', '1', 't')
    
    def get_sqalchemy_url(self) -> str:
        return f'postgresql+asyncpg://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}'
    
    def get_wg_post_cmd(self, var: str) -> str:
        return os.getenv('WG_POST_UP').replace('$WG_DEFAULT_ADDRESS', self.WG_DEFAULT_ADDRESS).replace('x//0', '0').replace('$WG_DEVICE', self.WG_DEVICE).replace('$WG_PORT', self.WG_PORT)

conf = Config()