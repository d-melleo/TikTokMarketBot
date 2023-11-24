from typing import Set

from aiogram import Bot, F, Router
from aiogram.filters import MagicData
from aiogram.types import Chat

from ..enums import markup, text



router = Router(name="private_banned")

_filters: Set[MagicData] = {
    MagicData(F.my_user.is_banned)
}

_exclude = ["update", "error"]
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)


### HANDLERS ###
@router.message()
async def banned(_, bot: Bot, event_chat: Chat) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.banned()
    )