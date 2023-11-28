from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from ...enums.private_chat_markup_data import PrivateChatMarkupData as MD


def send_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_(MD.SEND_VIDEO_LABEL),
        callback_data=MD.SEND_VIDEO_DATA))

    return keyboard.as_markup()
