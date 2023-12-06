"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""
import re
from typing import Dict
from textwrap import dedent

from aiogram.utils.i18n import gettext as _
from emoji import emojize


def ban(username: str, banned: bool = None) -> str:
    if banned:
        result = "has been banned."
    elif banned is None:
        result = "is you. You cannot ban yourself."
    else:
        result = "does not exist in your database. Cannot ban."

    return _(f"User with username @{username} {result}")


def incomplete_command(command: str) -> str:
    command = re.sub(r"/", "", command)
    command = re.sub(r"_", " ", command)
    return _(f"Please, enter a username you would like to {command}.")