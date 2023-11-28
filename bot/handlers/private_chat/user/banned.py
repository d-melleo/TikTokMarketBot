from aiogram import Bot, F, Router
from aiogram.filters import MagicData
from aiogram.types import Chat, Message

from ....messages.text import private_chat_text as T
from bot.tools.router_setup import register_filters

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_banned")

filters = {
    MagicData(F.my_user.is_banned)
}
# Register filters for this sub router.
register_filters(router, filters)


@router.message()
async def banned(message: Message, bot: Bot, event_chat: Chat) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.banned()
    )