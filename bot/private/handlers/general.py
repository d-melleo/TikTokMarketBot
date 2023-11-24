from typing import Set

from aiogram import Bot, F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import CallbackQuery, Chat, Message
from aiogram.enums.content_type import ContentType

from ...channels.admissions.handlers.general import post_video
from ..enums import markup, text
from ..enums.markup import SEND_VIDEO_DATA


router = Router(name="private_general")

_filters: Set[MagicData] = {
    MagicData(~F.my_user.is_banned)
}

_exclude = ["update", "error"]
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)



### HANDLERS ###

@router.message(Command("start"))
async def start(_, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.start(),
        reply_markup=markup.start()
    )


@router.callback_query(F.data == SEND_VIDEO_DATA)
async def request_video(_, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.request_video()
    )


@router.message((F.video.duration <= 62) & (~F.media_group_id))
async def received_video(message: Message, bot: Bot, event_chat: Chat):
    # Send a video to the Admissions channel
    await post_video(message, bot)

    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_video()
    )


@router.message((F.video.duration > 62) | (F.media_group_id) & (F.video))
async def received_video_long(_, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_video_long()
    )


@router.message(~F.content_type.in_({ContentType.TEXT, ContentType.VIDEO}))
async def received_other_media(_, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=text.received_other_media()
    )