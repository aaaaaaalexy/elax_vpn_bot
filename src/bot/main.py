import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from bot.middlewares import register_all_middlewires
from bot.handlers import register_all_handlers
from bot.database.models import async_main
from bot.database.requests import check_subscriptions
from bot.misc import bot_commands
from bot.utils import conf
from bot.wireguard import start_wireguard, stop_wireguard
from bot.payments import init_yookassa


async def scheduler(bot: Bot):
    while True:
        await check_subscriptions(bot)
        await asyncio.sleep(86400)  # need 86400


async def on_start_up(bot: Bot, dp: Dispatcher) -> None:
    await start_wireguard()
    
    init_yookassa()
    
    register_all_middlewires(dp)
    register_all_handlers(dp)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    
    await bot.set_my_commands(commands=commands_for_bot)

    asyncio.create_task(scheduler(bot))


async def start_bot() -> None:
    
    logging.basicConfig(level=logging.DEBUG)

    await async_main()

    bot = Bot(token=conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()

    await on_start_up(bot, dp)

    await dp.start_polling(bot, handle_signals=False)


async def stop_bot() -> None:
    await stop_wireguard()