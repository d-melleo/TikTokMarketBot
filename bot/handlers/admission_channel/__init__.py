from typing import List

from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import MagicData

from .admissions.handlers import router as admissions_main


# Parent router filters.
_filters = {
    MagicData(F.event_chat.type == ChatType.CHANNEL)
}

# Sub routers.
_routers: List[Router] = [
    admissions_main
]

# Create the parent router for all sub routers in for channel handlers.
router = Router(name="channels_root")
router.include_routers(*_routers)

_exclude = ["update", "error"]
# Register filters to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)



from typing import List, Dict

from aiogram import F, Router
from aiogram.filters import MagicData

from .general import router as admissions_general
from config import CHANNELS


ADMISSIONS_KEY = "admissions"

# Router filters
_filters = {
    MagicData(F.event_chat.id == CHANNELS[ADMISSIONS_KEY])
}

# Sub routers of the admissions channel.
_routers: List[Router] = [
    admissions_general
]

# Create the parent router for all sub routers in for the Admissions channel handlers.
router = Router(name="admissions_main")
router.include_routers(*_routers)

_exclude = ["update", "error"]
# Register filters to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)