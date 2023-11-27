from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..enums.markup_data import MarkupData as M


def post_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=M.VIDEO_LIKED_LABEL, callback_data=M.VIDEO_LIKED_DATA))
    keyboard.add(InlineKeyboardButton(text=M.VIDEO_DISLIKED_LABEL, callback_data=M.VIDEO_DISLIKED_DATA))

    return keyboard.as_markup()


def confirm_decision(callback_data: CallbackQuery) -> InlineKeyboardBuilder:
    if callback_data == M.VIDEO_LIKED_DATA:
        callback = M.CONFIRMED_LIKED_DATA
    elif callback_data == M.VIDEO_DISLIKED_DATA:
        callback = M.CONFIRMED_DISLIKED_DATA

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=M.CONFIRMED_LABEL, callback_data=callback))
    keyboard.add(InlineKeyboardButton(text=M.NOT_CONFIRMED_LABEL, callback_data=M.NOT_CONFIRMED_DATA))

    return keyboard.as_markup()