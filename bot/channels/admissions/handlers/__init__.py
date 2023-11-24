from typing import List, Dict

from aiogram import Router, F
from aiogram.filters import MagicData

from .general import router as admissions_general
from config import CHANNELS


ADMISSIONS_KEY = "admissions"
CHANNELS: Dict[str, int]

_filters = {
    MagicData(F.event_chat.id == CHANNELS[ADMISSIONS_KEY])
}

_routers: List[Router] = [
    admissions_general
]

router = Router(name="admissions_main")
router.include_routers(*_routers)

_exclude = ["update", "error"]
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)