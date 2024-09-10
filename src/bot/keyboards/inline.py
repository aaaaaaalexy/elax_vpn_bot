from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def get_keyboard(items: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=callback_data) 
         for text, callback_data in row_items] for row_items in items
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_keyboard_with_urls(items: list[list[tuple[tuple[str, str], str]]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=callback_data, url=url) 
         for (text, callback_data), url in row_items] for row_items in items
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_contact_keyboard(get_phone_number: str) -> InlineKeyboardMarkup:
    buttons = [[KeyboardButton(text=get_phone_number, request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard