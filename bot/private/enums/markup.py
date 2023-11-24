from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


SEND_VIDEO_DATA = "send_video"


def start() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_("Send a video"),
        callback_data=SEND_VIDEO_DATA))

    return keyboard.as_markup()
