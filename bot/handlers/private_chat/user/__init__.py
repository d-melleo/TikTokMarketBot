from typing import Dict, List, Tuple

from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import MagicData

from .banned import router as banned_router
from .user import router as user_router

from ..middlewares import _middlewares, INNER_MIDDLEWARE_KEY, OUTER_MIDDLEWARE_KEY


# Parent router filters.
_filters = {
    MagicData(F.event_chat.type == ChatType.PRIVATE)
}

# Sub routers.
_routers: List[Router] = [
    user_router,
    banned_router
]

# Create the parent router for all sub routers in for private handlers.
router = Router(name="private_root")
router.include_routers(*_routers)

_exclude = ["update", "error"]
# Register filters to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)

# Register middlewares to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        for scope, middlewares in _middlewares.items():
            for middleware in middlewares:
                if scope == OUTER_MIDDLEWARE_KEY:
                    observer_event.outer_middleware(middleware())
                elif scope == INNER_MIDDLEWARE_KEY:
                    observer_event.middleware(middleware())