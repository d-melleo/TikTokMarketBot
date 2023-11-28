from typing import Union

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Chat, Message

from ...enums.admissions_channel_markup_data import AdmissionsChannelMarkupData as MD
from ...messages.markups import admission_channel_markups as M
from ...messages.text import admission_channel_text as T
from config.environment_vars import CHANNELS
from db.userdata import UserData

ADMISSIONS_CHANNEL_ID: int = CHANNELS['admissions']

# Sub router of the parent Router(name="admissions_channel_root")
router = Router(name="admissions_channel_general")


async def post_video(
    message: Message,
    bot: Bot,
    my_user: UserData,
    channel_id: Union[int, str] = ADMISSIONS_CHANNEL_ID
) -> None:
    await bot.send_video(
        chat_id=channel_id,
        video=message.video.file_id,
        caption=T.post_video(message, my_user),
        reply_markup=M.post_video()
    )


@router.callback_query(F.data.in_({MD.VIDEO_LIKED_DATA, MD.VIDEO_DISLIKED_DATA}))
async def confirm_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=T.confirm_decision(callback_query),
        reply_markup=M.confirm_decision(callback_query.data)
    )


@router.callback_query(F.data.in_({MD.CONFIRMED_LIKED_DATA, MD.CONFIRMED_DISLIKED_DATA}))
async def confirmed_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=T.confirmed_decision(callback_query),
        reply_markup=None
    )


@router.callback_query(F.data == MD.NOT_CONFIRMED_DATA)
async def not_confirmed(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=T.not_confirmed(callback_query),
        reply_markup=M.post_video()
    )
