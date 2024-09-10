from .wireguard import WireGuard


wg = WireGuard()


async def start_wireguard() -> None:
    await wg.start()


async def stop_wireguard() -> None:
    await wg.stop()