from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def start() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_("Send a video"),
        callback_data="send_video"))

    return keyboard.as_markup()
