from aiogram import Dispatcher

from .handlers import routers
from .middlewares import ThrottlingMiddleware
from .tools.router_setup import register_middlewares


async def initialize() -> Dispatcher:
    """Initialize the aiogram Dispatcher with routers and middlewares.

    Returns:
        Dispatcher: The initialized aiogram Dispatcher.
    """
    dp = Dispatcher(name="dispatcher")  # Create dispatcher instance (it's the root/main Router)
    dp.include_routers(*routers)  # Register sub routers
    register_middlewares(
        router=dp,
        include_events=["update"],
        outer=(ThrottlingMiddleware,)
    )

    return dp