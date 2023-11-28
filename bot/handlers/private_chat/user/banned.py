from typing import Set

from aiogram import Bot, F, Router
from aiogram.filters import MagicData
from aiogram.types import Chat, Message

from ..content import text

# Sub router of the parent Router(name="private_root")
router = Router(name="private_banned")

# Filters for this sub router
_filters: Set[MagicData] = {
    MagicData(F.my_user.is_banned)
}

_exclude = ["update", "error"]
# Register filters to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)


@router.message()
async def banned(message: Message, bot: Bot, event_chat: Chat) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.banned()
    )