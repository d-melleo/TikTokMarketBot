from typing import Dict, List, Tuple

from aiogram import Router, F, BaseMiddleware
from aiogram.filters import MagicData
from aiogram.enums.chat_type import ChatType

from .general import router as general_router
from .banned import router as banned_router

from ..middlewares import OUTER_MIDDLEWARE_KEY, INNER_MIDDLEWARE_KEY, _middlewares



_filters = {
    MagicData(F.event_chat.type == ChatType.PRIVATE)
}

_routers: List[Router] = [
    general_router,
    banned_router
]

router = Router(name="private_root")
router.include_routers(*_routers)


_exclude = ["update", "error"]

for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)

for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        for scope, middlewares in _middlewares.items():
            for middleware in middlewares:
                if scope == OUTER_MIDDLEWARE_KEY:
                    observer_event.outer_middleware(middleware())
                elif scope == INNER_MIDDLEWARE_KEY:
                    observer_event.middleware(middleware())