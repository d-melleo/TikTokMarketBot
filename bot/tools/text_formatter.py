import string
from typing import Any, Dict

from aiogram.utils.formatting import Text


def text_formatter(text: str, values: Dict[str, Any]) -> Dict[str, Any]:
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