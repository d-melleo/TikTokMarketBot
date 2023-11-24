import re
from textwrap import dedent

from aiogram.types import Message, CallbackQuery



"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""



def post_video(message: Message) -> str:
    instructions = "\n↪ Натисни 👍, щоб повідомити користувачу, що відео сподобалося, або 👎, що не сподобалося."

    text = dedent('''\
Надійшло нове відео! 🎉

Користувач: @{username}
Ім'я: {name}
Дата: {date}''').format(
    username=message.from_user.username,
    name=f'{message.from_user.first_name} {message.from_user.last_name}',
    date=message.date.strftime('%d.%m.%Y'))

    if message.text:
        text+="\nКоментарій: {}".format(message.text)

    output_text = f'{text}\n{instructions}'

    return output_text


def confirm_decision(callback_query: CallbackQuery) -> str:
    original_text: str = callback_query.message.caption.split("\n↪ ")[:-1][0]

    instructions = "\n↪ Повідомити користувачу, що відео Вам {}сподобалось?"
    
    if callback_query.data == "video_liked": instructions = instructions.format('')
    if callback_query.data == "video_disliked": instructions = instructions.format('не ')

    output_text = f'{original_text}{instructions}'

    return output_text


def confirmed_decision(callback_query: CallbackQuery) -> str:
    me: str = callback_query.from_user.username
    original_text: str = callback_query.message.caption.split("\n↪ ")[:-1][0]
    username: str = re.findall(r"@\w+", original_text)[0]

    instructions = "{emoji} @{me} сповістив(-ла) {username}, що відео {no}сподобалось."
    
    if callback_query.data == "confirmed_liked":
        instructions = instructions.format(emoji='✅', me=me, username=username, no='')
    elif callback_query.data == "confirmed_disliked":
        instructions = instructions.format(emoji='❌', me=me, username=username, no='не ')

    output_text = f'{original_text}\n{instructions}'

    return output_text


def not_confirmed(callback_query: CallbackQuery) -> str:
    original_text: str = callback_query.message.caption.split("\n↪ ")[:-1][0]
    instructions = "\n↪ Натисни 👍, щоб повідомити користувачу, що відео сподобалося, або 👎, що не сподобалося."

    output_text = f'{original_text}{instructions}'
    return output_text