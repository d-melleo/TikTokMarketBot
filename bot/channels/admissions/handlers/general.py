from typing import Union

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Chat, Message

from config import CHANNELS
from ..enums import markup, text
from ..enums.markup import (
    VIDEO_LIKED_DATA, VIDEO_DISLIKED_DATA,
    CONFIRMED_LIKED_DATA, CONFIRMED_DISLIKED_DATA,
    NOT_CONFIRMED_DATA
)


ADMISSIONS_CHANNEL_ID: int = CHANNELS['admissions']

router = Router(name="admissions_general")


### HANDLERS ###

async def post_video(
    message: Message,
    bot: Bot,
    channel_id: Union[int, str] = ADMISSIONS_CHANNEL_ID):
    await bot.send_video(
        chat_id=channel_id,
        video=message.video.file_id,
        caption=text.post_video(message),
        reply_markup=markup.post_video()
    )


@router.callback_query(F.data.in_({VIDEO_LIKED_DATA, VIDEO_DISLIKED_DATA}))
async def confirm_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.confirm_decision(callback_query),
        reply_markup=markup.confirm_decision(callback_query.data)
    )


@router.callback_query(F.data.in_({CONFIRMED_LIKED_DATA, CONFIRMED_DISLIKED_DATA}))
async def confirmed_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.confirmed_decision(callback_query),
        reply_markup=None
    )


@router.callback_query(F.data == NOT_CONFIRMED_DATA)
async def not_confirmed(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.not_confirmed(callback_query),
        reply_markup=markup.post_video()
    )
