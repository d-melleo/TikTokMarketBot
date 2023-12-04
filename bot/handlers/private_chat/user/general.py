from aiogram import Bot, F, Router
from aiogram.enums import ContentType, MessageEntityType
from aiogram.filters import Command, MagicData
from aiogram.types import CallbackQuery, Chat, Message, User

from ....messages.markups import private_chat_markup as M
from ....messages.text import private_chat_text as T
from ....enums import PrivateChatMarkupData as MD
from bot.tools.router_setup import register_filters
from db.userdata import UserData

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_general")

filters = {
    MagicData(~F.my_user.is_banned)
}
# Register filters for this sub router.
register_filters(router, filters)


@router.message(Command("start"))
async def start(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.start(),
        reply_markup=M.send_video()
    )


@router.callback_query(F.data == MD.SEND_VIDEO_DATA)
async def request_video(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.request_video()
    )


@router.message((F.video.duration <= 62) & (~F.media_group_id))
async def received_video(
    message: Message, bot: Bot, event_chat: Chat, event_from_user: User):
    from ...admission_channel.general import post_video

    # Send a video to the Admissions channel
    await post_video(message, bot, event_from_user)

    await bot.send_message(
        chat_id=event_chat.id,
        text=T.received_video()
    )


@router.message((F.video.duration > 62) | (F.media_group_id) & (F.video))
async def received_video_long(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.received_video_long()
    )


@router.message(~F.content_type.in_({ContentType.TEXT, ContentType.VIDEO}))
async def received_other_media(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.received_other_media()
    )


async def notify_user_desicion(message: Message, bot: Bot, decision: str):
    for entity in message.caption_entities:
        if entity.type == MessageEntityType.TEXT_MENTION:
            video_from_user: User = entity.user
    
    await bot.send_message(
        chat_id=video_from_user.id,
        text=T.notify_user_desicion(decision)
    )