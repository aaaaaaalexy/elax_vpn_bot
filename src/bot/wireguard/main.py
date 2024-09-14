from .wireguard import WireGuard
from bot.utils import debug


wg = WireGuard()


async def start_wireguard() -> None:
    await wg.start()
    debug('WireGuard started...')


async def stop_wireguard() -> None:
    await wg.stop()
    debug('WireGuard stoped.')