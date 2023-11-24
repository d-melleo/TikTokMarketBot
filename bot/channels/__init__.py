from typing import List

from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.enums.chat_type import ChatType

from .admissions.handlers import router as admissions_main


_filters = {
    MagicData(F.event_chat.type == ChatType.CHANNEL)
}

_routers: List[Router] = [
    admissions_main
]

router = Router(name="channels_root")
router.include_routers(*_routers)

_exclude = ["update", "error"]
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)