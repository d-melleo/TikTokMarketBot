from typing import Union

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Chat, Message

from ..content import markup, text
from ..enums.markup_data import MarkupData as M
from config import CHANNELS
from db.userdata import UserData

ADMISSIONS_CHANNEL_ID: int = CHANNELS['admissions']
router = Router(name="admissions_general")


async def post_video(
    message: Message,
    bot: Bot,
    my_user: UserData,
    channel_id: Union[int, str] = ADMISSIONS_CHANNEL_ID
) -> None:

    await bot.send_video(
        chat_id=channel_id,
        video=message.video.file_id,
        caption=text.post_video(message, my_user),
        reply_markup=markup.post_video()
    )


@router.callback_query(F.data.in_({M.VIDEO_LIKED_DATA, M.VIDEO_DISLIKED_DATA}))
async def confirm_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.confirm_decision(callback_query),
        reply_markup=markup.confirm_decision(callback_query.data)
    )


@router.callback_query(F.data.in_({M.CONFIRMED_LIKED_DATA, M.CONFIRMED_DISLIKED_DATA}))
async def confirmed_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.confirmed_decision(callback_query),
        reply_markup=None
    )


@router.callback_query(F.data == M.NOT_CONFIRMED_DATA)
async def not_confirmed(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=text.not_confirmed(callback_query),
        reply_markup=markup.post_video()
    )
