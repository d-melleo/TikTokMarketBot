"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""

import re
from textwrap import dedent

from aiogram.types import Message, CallbackQuery
from emoji import emojize

from ...enums.admissions_channel_markup_data import AdmissionsChannelMarkupData as MD
from db.userdata import UserData

INSTRUCTIONS_DELIMITER = emojize(":left_arrow_curving_right:")


def post_video(message: Message, my_user: UserData) -> str:
    instructions = """\
{delimiter} Натисни {yes}, щоб сповістити користувача, що відео сподобалось, \
або {no}, що не сподобалось.\
"""\
    .format(
        delimiter=INSTRUCTIONS_DELIMITER,
        yes=MD.VIDEO_LIKED_LABEL,
        no=MD.VIDEO_DISLIKED_LABEL
    )

    text = dedent(
"""\
Надійшло нове відео! 🎉

Користувач: @{username}
Ім'я: {name}
Дата: {date}\
"""
).format(
    username=my_user.username,
    name=my_user.full_name,
    date=message.date.strftime('%d.%m.%Y'))

    if message.text:
        text+="\nКоментарій: {}".format(message.text)

    output_text = f'{text}\n{instructions}'
    return output_text


def confirm_decision(callback_query: CallbackQuery) -> str:
    original_text: str = callback_query.message.caption.split(INSTRUCTIONS_DELIMITER)[:-1][0]

    instructions = """\
{delimiter} Повідомити користувачу, що відео Вам {no}сподобалось?\
"""\
    .format(
        delimiter=INSTRUCTIONS_DELIMITER,
    )

    if callback_query.data == MD.VIDEO_LIKED_DATA:
        instructions = instructions.format('')
    if callback_query.data == MD.VIDEO_DISLIKED_DATA:
        instructions = instructions.format('не ')

    output_text = f'{original_text}{instructions}'
    return output_text


def confirmed_decision(callback_query: CallbackQuery) -> str:
    original_text: str = callback_query.message.caption.split(INSTRUCTIONS_DELIMITER)[:-1][0]
    me: str = callback_query.from_user.username  # Get username of the user's pressed teh button
    username: str = re.findall(r"@\w+", original_text)[0]  # Get username of the user's sent a video

    instructions = """\
{emoji} @{me} сповістив(-ла) {username}, що відео {no}сподобалось.\
"""\
    .format(
        me=me,
        username=username,
    )

    if callback_query.data == MD.CONFIRMED_LIKED_DATA:
        instructions = instructions.format(emoji=emojize(':check_mark:'), no='')
    elif callback_query.data == MD.CONFIRMED_DISLIKED_DATA:
        instructions = instructions.format(emoji=emojize(':cross_mark:'), no='не ')

    output_text = f'{original_text}{instructions}'
    return output_text


def not_confirmed(callback_query: CallbackQuery) -> str:
    original_text: str = callback_query.message.caption.split(INSTRUCTIONS_DELIMITER)[:-1][0]

    instructions = """\
{delimiter} Натисни {yes}, щоб сповістити користувача, що відео сподобалось, \
або {no}, що не сподобалось.\
"""\
    .format(
        delimiter=INSTRUCTIONS_DELIMITER,
        yes=MD.VIDEO_LIKED_LABEL,
        no=MD.VIDEO_DISLIKED_LABEL
    )

    output_text = f'{original_text}{instructions}'
    return output_text