"""
    - Pybabel commands:
        pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
        pybabel extract --input-dirs=. -o locales/messages.pot
        pybabel update -d locales -D messages -i locales/messages.pot
        pybabel compile -d locales -D messages
"""

import re

from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text
from emoji import emojize

from ...enums import AdmissionsChannelMarkupData as MD
from db.userdata import UserData


# Decorator, merges text with instructions
def formatter(func) -> str:
    video_caption=\
"""\
Надійшло нове відео! {emj}

Користувач: @{username}
Ім'я: {name}
Дата: {date}\
"""

    def wrapper(*args, **kwargs) -> str:
        # Delimiter will separate caption from instructions
        delimiter = "{}{}".format(emojize(":left_arrow_curving_right:"), " ")  # [↪️+intentional wtitespace]

        # Unpack arguments from the function
        data = func(*args, **kwargs)
        instr = data.get("instr")

        if isinstance(data.get("message"), Message):
            message: Message = data["message"]
            if message.video:
                
                my_user: UserData = data["my_user"]
                text = video_caption.format(
                    emj=emojize(":party_popper:"),
                    username=my_user.username,
                    name=my_user.full_name,
                    date=message.date.strftime('%d.%m.%Y')
                )
                if message.caption:
                    text += f"\nКоментарій: {message.caption}"
        else:
            text = data["text"]

        # Remove old instructions, whitespaces, more than one blank line in a row
        text = text.split(delimiter)[0].strip('\n').strip()

        if data.get("delimiter"):
            delimiter = data["delimiter"]

        # Add delimiter to the instructions
        instr = f"{delimiter} {instr}".strip()
        # Merge new instructions to the old text
        output_text = f"{text}{instr}"
        # Append a blank line between the text and instructions
        output_text = re.sub(delimiter, "\n"*2 + delimiter, output_text)
        # Remove blanklines, if more than one in a row
        output_text = re.sub(r"\n{3,}", "\n"*2, output_text)

        return output_text

    return wrapper


@formatter
def post_video(message: Message, my_user: UserData):
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
        "my_user": my_user
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
        "text": callback_query.message.caption
    }


@formatter
def confirmed_decision(callback_query: CallbackQuery):
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
def not_confirmed(callback_query: CallbackQuery):
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