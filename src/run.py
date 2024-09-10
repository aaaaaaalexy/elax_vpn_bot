import asyncio
from bot import start_bot, stop_bot


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(stop_bot())
        print('Bot stopped.')