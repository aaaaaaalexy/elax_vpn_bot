from aiogram import types
from aiogram.filters.command import CommandObject
from aiogram.utils.formatting import Text, Italic, BotCommand

import bot.database.requests as rq
from bot.misc.bot_commands import bot_commands
from bot.misc.messages import help_message, help_all_message, not_registered_message
from bot.keyboards import go_home_keyboard, start_keyboard


async def cmd_help(message: types.Message, command:CommandObject):
    if await rq.user_is_registered(tg_id=message.from_user.id):
        if command.args:
            if command.args == 'all':
                return await message.answer(help_all_message)
                    
            else:
                for cmd in bot_commands:
                    if cmd[0] == command.args:
                        content = Text(BotCommand(f'/{cmd[0]}'), f' - {cmd[1]}\n', Italic(cmd[2]))
                        return await message.answer(content)
                    
                return await message.answer('Команда не найдена')
        
        return await message.answer(help_message)
    else:
        await message.answer(not_registered_message,
                             reply_markup=start_keyboard)


async def callback_help(callback: types.CallbackQuery) -> None:
    await callback.message.answer(help_message,
                                     reply_markup=go_home_keyboard)
    await callback.answer()


async def callback_help_all(callback: types.CallbackQuery) -> None:
    await callback.message.answer(help_all_message,
                                  reply_markup=go_home_keyboard)
    await callback.answer()
