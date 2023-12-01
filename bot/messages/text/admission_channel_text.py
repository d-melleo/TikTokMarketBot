"""
    - Pybabel commands:
        pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
        pybabel extract --input-dirs=. -o locales/messages.pot
        pybabel update -d locales -D messages -i locales/messages.pot
        pybabel compile -d locales -D messages
"""

from datetime import datetime
import string
from typing import Any, Dict
import re

from aiogram.enums import MessageEntityType
from aiogram.types import Message, MessageEntity, CallbackQuery, User
from aiogram.utils.formatting import Text, Bold, TextMention, as_list, as_line
from emoji import emojize

from ...enums import AdmissionsChannelMarkupData as MD
from db.userdata import UserData


def _get_caption(user: User, date: datetime) -> Text:
    values = {
        "date": "date",
        "name": "name",
        "emoji": "emoji",
        "username": lambda: TextMention(user.username, user=user)
    }

    text = """\
Надійшло нове відео! {emoji}

Користувач: {username}
Ім'я: {name}
Дата: {date}
"""

    output = []  # Text arguments with resolved placeholders

    for part in string.Formatter().parse(text):
        # Separating text from placeholders
        literal_text, placeholder = part[:2]
        if literal_text:
            # Append plain text into the list
            output.append(literal_text)
        if placeholder:
            # Get value fro the placeholder and execute is calalble
            value = values[placeholder]
            if callable(value):
                value = value()
            output.append(value)

    return Text(*output).as_kwargs()


# Decorator, merges text with instructions
def formatter(func) -> str:
    def wrapper(*args, **kwargs) -> str:
        # Unpack arguments from the function
        data: Dict[str, Any] = func(*args, **kwargs)

        # Instructions for administrators in channel
        instr: str = data.get("instr")
        # Initial messasge instance for the sent video
        message: Message = data.get("message")
        # User instance of the user that has initially sent a video in Bot
        user: User = data.get("video_from_user")

        # Get user's instance from caption mention entity
        if not user:
            for entity in message.caption_entities:
                if entity.type == MessageEntityType.TEXT_MENTION:
                    user: User = entity.user

        text = _get_caption(user, date=message.date.strftime('%d.%m.%Y'))
        return text

    return wrapper


@formatter
def post_video(message: Message, video_from_user: User):
    # Instructions
    instr = """\
Натисни {yes}, щоб сповістити користувача, що відео сподобалось, \
або {no}, що не сподобалось.\
"""

    instr = instr.format(
        yes=MD.VIDEO_LIKED_LABEL.value,
        no=MD.VIDEO_DISLIKED_LABEL.value
    )

    return {
        "instr": instr,
        "message": message,
        "video_from_user": video_from_user,
        }


@formatter
def confirm_decision(callback_query: CallbackQuery):
    # Instructions
    instr = "Повідомити користувачу, що відео Вам {no}сподобалось?"

    if callback_query.data == MD.VIDEO_LIKED_DATA:
        instr = instr.format(no='')
    elif callback_query.data == MD.VIDEO_DISLIKED_DATA:
        instr = instr.format(no='не ')

    return {
        "instr": instr,
        "message": callback_query.message
        }


@formatter
def confirmed_decision(callback_query: CallbackQuery, video_from_user: User):
    # Instructions
    instr = "@{me} сповістив(-ла) користувача, що відео {no}сподобалось."

    if callback_query.data == MD.CONFIRMED_LIKED_DATA:
        no = ''
        emj = emojize(":check_mark_button:")
    elif callback_query.data == MD.CONFIRMED_DISLIKED_DATA:
        no = 'не '
        emj = emojize(":cross_mark:")

    instr = instr.format(
        me= callback_query.from_user.username,
        no=no
    )

    return {
        "instr": instr,
        "text": callback_query.message.caption,
        "delimiter": emj
    }


@formatter
def not_confirmed(callback_query: CallbackQuery, video_from_user: User):
    # Instructions
    instr = """\
Натисни {yes}, щоб сповістити користувача, що відео сподобалось, \
або {no}, що не сподобалось.\
"""

    instr = instr.format(
        yes=MD.VIDEO_LIKED_LABEL.value,
        no=MD.VIDEO_DISLIKED_LABEL.value
    )

    return {
        "instr": instr,
        "text": callback_query.message.caption
    }