from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import MagicData

from ..admission_channel.general import router as admissions_channel_general
from ...middlewares import LocalizationMiddleware
from ...tools.router_setup import register_filters, register_middlewares
from config.environment_vars import CHANNELS

ADMISSIONS_KEY = "admissions"

# The parent admissions's channel router
router = Router(name="admissions_channel_root")

filters = {
    MagicData(F.event_chat.type == ChatType.CHANNEL),
    MagicData(F.event_chat.id == CHANNELS[ADMISSIONS_KEY])
}

register_filters(router, filters)

router.include_routers(
    admissions_channel_general
)

register_middlewares(
    router=router,
    inner=(
        LocalizationMiddleware,
    )
)