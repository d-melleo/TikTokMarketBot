from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ...enums import AdmissionsChannelMarkupData as MD


def post_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=MD.VIDEO_LIKED_LABEL, callback_data=MD.VIDEO_LIKED_DATA))
    keyboard.add(InlineKeyboardButton(text=MD.VIDEO_DISLIKED_LABEL, callback_data=MD.VIDEO_DISLIKED_DATA))

    return keyboard.as_markup()


def confirm_decision(callback_data: CallbackQuery) -> InlineKeyboardBuilder:
    if callback_data == MD.VIDEO_LIKED_DATA:
        callback = MD.CONFIRMED_LIKED_DATA
    elif callback_data == MD.VIDEO_DISLIKED_DATA:
        callback = MD.CONFIRMED_DISLIKED_DATA

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=MD.CONFIRMED_LABEL, callback_data=callback))
    keyboard.add(InlineKeyboardButton(text=MD.NOT_CONFIRMED_LABEL, callback_data=MD.NOT_CONFIRMED_DATA))

    return keyboard.as_markup()