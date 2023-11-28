from typing import Set

from aiogram import Bot, F, Router
from aiogram.enums.content_type import ContentType
from aiogram.filters import Command, MagicData
from aiogram.types import CallbackQuery, Chat, Message

from ...channels.admissions.handlers.general import post_video
from ..content import markup, text
from ..enums.markup_data import MarkupData as M
from db.userdata import UserData

# Sub router of the parent Router(name="private_root")
router = Router(name="private_user")

# Filters for this sub router
_filters: Set[MagicData] = {
    MagicData(~F.my_user.is_banned)
}

_exclude = ["update", "error"]
# Register filters to all events that are not in _exclude.
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)


@router.message(Command("start"))
async def start(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.start(),
        reply_markup=markup.send_video()
    )


@router.callback_query(F.data == M.SEND_VIDEO_DATA)
async def request_video(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.request_video()
    )


@router.message((F.video.duration <= 62) & (~F.media_group_id))
async def received_video(message: Message, bot: Bot, event_chat: Chat, my_user: UserData):
    # Send a video to the Admissions channel
    await post_video(message, bot, my_user)

    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_video()
    )


@router.message((F.video.duration > 62) | (F.media_group_id) & (F.video))
async def received_video_long(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_video_long()
    )


@router.message(~F.content_type.in_({ContentType.TEXT, ContentType.VIDEO}))
async def received_other_media(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_other_media()
    )