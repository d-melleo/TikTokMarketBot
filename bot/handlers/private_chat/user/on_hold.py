from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.filters import MagicData
from aiogram.types import Chat, Message

from ....messages.text import private_chat_text as T
from bot.tools.router_setup import register_filters
from db.userdata import UserData

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_on_hold")

filters = {
    (MagicData(F.my_user.hold_until > F.current_utc_time))
}
# Register filters for this sub router.
register_filters(router, filters)


@router.message()
async def on_hold(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    my_user: UserData,
    current_utc_time: datetime
) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.on_hold(my_user.hold_timer(current_utc_time))
    )