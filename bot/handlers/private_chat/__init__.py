from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import MagicData

from .user.general import router as private_chat_general
from .user.banned import router as private_chat_banned

from ...middlewares import (
    DatabaseMiddleware,
    CommandsMiddleware,
    LocalizationMiddleware
)
from ...tools.router_setup import register_filters, register_middlewares

# The parent router for private chat sub routers
router = Router(name="private_chat_root")

filters = {
    MagicData(F.event_chat.type == ChatType.PRIVATE)
}

register_filters(router, filters)

router.include_routers(
    private_chat_general,
    private_chat_banned
)

register_middlewares(
    router=router,
    outer=(
        DatabaseMiddleware,
    ),
    inner=(
        LocalizationMiddleware,
        CommandsMiddleware
    )
)