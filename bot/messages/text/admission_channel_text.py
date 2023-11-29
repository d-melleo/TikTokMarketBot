"""
    - Pybabel commands:
        pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
        pybabel extract --input-dirs=. -o locales/messages.pot
        pybabel update -d locales -D messages -i locales/messages.pot
        pybabel compile -d locales -D messages
"""

from enum import Enum
import re
from textwrap import dedent

from aiogram.types import Message, CallbackQuery
from emoji import emojize

from ...enums.admissions_channel_markup_data import AdmissionsChannelMarkupData as MD
from db.userdata import UserData



# Decorator, merges text with instructions
def formatting(func) -> str:
    INSTR_DELIMITER = "{}{}".format(
        emojize(":left_arrow_curving_right:"),  # Emoji: ↪️
        " "  # Intentional whitespace
        )

    def wrapper(*args, **kwargs) -> str:
        # Unpack arguments from the function
        data = func(*args, **kwargs)
        instr = data["instr"]

        if data["message"]:
            if data["message"].video:
                message: Message = data["message"]
                my_user: UserData = data["my_user"]

                text =\
"""\
Надійшло нове відео! {emj}

Користувач: @{username}
Ім'я: {name}
Дата: {date}\
"""\
.format(
    emj=emojize(":party_popper:"),
    username=my_user.username,
    name=my_user.full_name,
    date=message.date.strftime('%d.%m.%Y'))

        else:
            text = data["text"]

        # Add delimiter to the instructions
        instr = f"{INSTR_DELIMITER} {instr}"
        # Remove old instructions, whitespaces, more than one blank line in a row
        text = text.split(INSTR_DELIMITER)[0].strip('\n').strip()
        # Merge new instructions to the old text
        output_text = f"{text}{instr}"
        # Append a blank line between the text and instructions
        output_text = re.sub(INSTR_DELIMITER, "\n"*2 + INSTR_DELIMITER, output_text)
        # Remove blanklines, if more than one in a row
        output_text = re.sub(r"\n{3,}", "\n"*2, output_text)

        return output_text

    return wrapper


@formatting
def post_video(message: Message, my_user: UserData) -> str:
    # Instructions
    instr = """\
Натисни {yes}, щоб сповістити користувача, що відео сподобалось, або {no}, що не сподобалось.\
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