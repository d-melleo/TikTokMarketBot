"""
    - Pybabel commands:
        pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
        pybabel extract --input-dirs=. -o locales/messages.pot
        pybabel update -d locales -D messages -i locales/messages.pot
        pybabel compile -d locales -D messages
"""

from datetime import datetime
import re
from typing import Any, Dict

from aiogram.types import CallbackQuery, Message, User
from aiogram.utils.formatting import Italic, Spoiler, TextMention
from emoji import emojize

from ...enums import AdmissionsChannelMarkupData as MD
from ...tools.text_formatter import text_formatter


# Decorator, merges text with instructions
def _get_caption(func) -> Dict[str, Any]:
    video_caption=\
"""\
Надійшло нове відео! {emoji}

Користувач: {username}
Ім'я: {name}
{utc}: {date}\
"""

    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        # Delimiter will separate caption from instructions
        # By default: ↪️+intentional wtitespace
        delimiter = "{}{}".format(emojize(":left_arrow_curving_right:"), " ")

        # Unpack arguments from the function
        data: Dict[str, Any] = func(*args, **kwargs)
        # Get new instructions
        instr = data.get("instr")
        # Initial messasge instance for the sent video
        event: Message | CallbackQuery = data.get("event")
        # User instance of the user that has initially sent a video in Bot
        user: User = data.get("video_from_user")

        # Initial post is built on a template
        if isinstance(event, Message):
            if event.video:
                text = video_caption
                if event.caption:
                    text += "\n" + "Коментарій: {comment}"
                text += f"\n\n{delimiter}{instr}"

                return text_formatter(
                    text,
                    values={
                        "emoji": emojize(":party_popper:"),
                        "username": lambda: TextMention(f"@{user.username}", user=user),
                        "name": lambda: TextMention(user.full_name, user=user),
                        "utc": Italic("Дата (UTC)"),
                        "date": data.get("current_utc_time", event.date).strftime("%d.%m.%Y %H:%M"),
                        "comment": lambda: Spoiler(event.caption)
                    }
                )

        elif isinstance(event, CallbackQuery):
            # Initial text is being reused and insructions replaced
            text = event.message.caption
            entities = event.message.caption_entities
            # Remove old instructions, whitespaces and blank lines
            text = text.split(delimiter)[0].strip('\n').strip()
            # Replace delimiter in final message edit
            delimiter = data.get("delimiter", delimiter)
            # Merge new instructions with the old text
            output_text = f"{text}\n\n{delimiter}{instr}"
            # Remove blanklines, if more than one in a row
            output_text = re.sub(r"\n{3,}", "\n"*2, output_text)

            return {
                "text": output_text,
                "entities": entities
            }

    return wrapper


@_get_caption
def post_video(
    message: Message,
    video_from_user: User,
    current_utc_time: datetime
) -> Dict[str, Any]:
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
        "event": message,
        "video_from_user": video_from_user,
        "current_utc_time": current_utc_time
        }


@_get_caption
def confirm_decision(callback_query: CallbackQuery) -> Dict[str, Any]:
    # Instructions
    instr = "Повідомити користувачу, що відео Вам {no}сподобалось?"

    if callback_query.data == MD.VIDEO_LIKED_DATA:
        instr = instr.format(no='')
    elif callback_query.data == MD.VIDEO_DISLIKED_DATA:
        instr = instr.format(no='не ')

    return {
        "instr": instr,
        "event": callback_query
        }


@_get_caption
def confirmed_decision(callback_query: CallbackQuery) -> Dict[str, Any]:
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
        "event": callback_query,
        "delimiter": emj
    }


@_get_caption
def not_confirmed(callback_query: CallbackQuery) -> Dict[str, Any]:
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
        "event": callback_query
    }