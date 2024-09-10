from aiogram import types
from aiogram.filters.command import CommandObject
from aiogram.utils.formatting import Text, Italic, BotCommand

from bot.misc.bot_commands import bot_commands
from bot.misc.messages import help_message, help_all_message, help_connect_message


async def cmd_help(message: types.Message, command:CommandObject):
    if command.args:
        if command.args == 'all':
            return await message.answer(help_all_message)
        
        elif command.args == 'connect':
            return await message.answer(help_connect_message,
                                        link_preview_options=types.LinkPreviewOptions(is_disabled=True,
                                                                                      show_above_text=False))
        
        else:
            for cmd in bot_commands:
                if cmd[0] == command.args:
                    content = Text(BotCommand(f'/{cmd[0]}'), f' - {cmd[1]}\n', Italic(cmd[2]))
                    return await message.answer(content)
                
            return await message.answer('Команда не найдена')
    
    return await message.answer(help_message)


async def callback_help(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(help_message,
                                     reply_markup=callback.message.reply_markup)
    await callback.answer()


async def callback_help_all(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(help_all_message,
                                     reply_markup=callback.message.reply_markup,
                                     link_preview_options=types.LinkPreviewOptions(is_disabled=True))
    await callback.answer()
