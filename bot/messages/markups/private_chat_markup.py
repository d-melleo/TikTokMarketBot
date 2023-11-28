from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from ..enums.markup_data import MarkupData as M


def send_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_(M.SEND_VIDEO_LABEL),
        callback_data=M.SEND_VIDEO_DATA))

    return keyboard.as_markup()
