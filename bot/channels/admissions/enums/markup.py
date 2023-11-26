from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from emoji import emojize


VIDEO_LIKED_DATA = "video_liked"
VIDEO_DISLIKED_DATA = "video_disliked"
CONFIRMED_LIKED_DATA = "confirmed_liked"
CONFIRMED_DISLIKED_DATA = "confirmed_disliked"
NOT_CONFIRMED_DATA = "not_confirmed"


def post_video() -> InlineKeyboardBuilder:
    LBL_YES = emojize(":thumbs_up:")
    LBL_NO = emojize(":thumbs_down:")

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=LBL_YES, callback_data=VIDEO_LIKED_DATA))
    keyboard.add(InlineKeyboardButton(text=LBL_NO, callback_data=VIDEO_DISLIKED_DATA))

    return keyboard.as_markup()


def confirm_decision(callback_data: CallbackQuery) -> InlineKeyboardBuilder:
    LBL_YES = "Так"
    LBL_NO = "Ні"

    if callback_data == VIDEO_LIKED_DATA: callback = CONFIRMED_LIKED_DATA
    elif callback_data == VIDEO_DISLIKED_DATA: callback = CONFIRMED_DISLIKED_DATA

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=LBL_YES, callback_data=callback))
    keyboard.add(InlineKeyboardButton(text=LBL_NO, callback_data=NOT_CONFIRMED_DATA))

    return keyboard.as_markup()