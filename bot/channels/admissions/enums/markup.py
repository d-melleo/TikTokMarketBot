from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def post_video() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="👍", callback_data="video_liked"))
    keyboard.add(InlineKeyboardButton(text="👎", callback_data="video_disliked"))

    return keyboard.as_markup()


def confirm_decision(callback_data: str) -> InlineKeyboardBuilder:
    if callback_data == "video_liked": callback = "confirmed_liked"
    elif callback_data == "video_disliked": callback = "confirmed_disliked"

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Так", callback_data=callback))
    keyboard.add(InlineKeyboardButton(text="Ні", callback_data="not_confirmed"))

    return keyboard.as_markup()