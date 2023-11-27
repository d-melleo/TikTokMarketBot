from typing import Any, Dict, List, Tuple, Union

from aiogram import Dispatcher, Router

from .channels import router as channels_router
from .private.handlers import router as private_router
from .throttling import ThrottlingMiddleware

OUTER_MIDDLEWARE_KEY = "outer"
INNER_MIDDLEWARE_KEY = "inner"

_middlewares: Dict[str, Tuple[Union[ThrottlingMiddleware, Any]]] = {
    OUTER_MIDDLEWARE_KEY: (
        ThrottlingMiddleware,
    ),
    INNER_MIDDLEWARE_KEY: (
        # No middlewares added to 'inner' scope
    ),
}

_routers: List[Router] = [
    private_router,
    channels_router
]

_include = ["update"]

async def initialize() -> Dispatcher:
    """Initialize the aiogram Dispatcher with routers and middlewares.

    Returns:
        Dispatcher: The initialized aiogram Dispatcher.
    """
    dp = Dispatcher()  # Create dispatcher instance (the root/main Router)
    dp.include_routers(*_routers)  # Register sub routers

    # Register middlewares
    for observer_name, observer_event in dp.observers.items():
        if observer_name in _include:
            for scope, middlewares in _middlewares.items():
                for middleware in middlewares:
                    if scope == OUTER_MIDDLEWARE_KEY:
                        observer_event.outer_middleware(middleware())
                    elif scope == INNER_MIDDLEWARE_KEY:
                        observer_event.middleware(middleware())

    return dp