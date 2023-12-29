from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from ...enums import PrivateChatMarkupData as MD


def send_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_("Send a video"),
        callback_data=MD.SEND_VIDEO_DATA))

    return keyboard.as_markup()


def language() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=_("English 🇬🇧"),
        callback_data=MD.EN_LANGUAGE_DATA))
    keyboard.row(InlineKeyboardButton(
        text=_("Polish 🇵🇱"),
        callback_data=MD.PL_LANGUAGE_DATA))
    keyboard.row(InlineKeyboardButton(
        text=_("Ukrainian 🇺🇦"),
        callback_data=MD.UK_LANGUAGE_DATA))

    return keyboard.as_markup()