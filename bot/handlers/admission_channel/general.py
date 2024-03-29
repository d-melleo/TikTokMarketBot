from datetime import datetime
from typing import Any, Dict, Union

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Chat, Message, User

from ...enums import AdmissionsChannelFlags as AF
from ...enums import AdmissionsChannelMarkupData as MD
from ...messages.markups import admission_channel_markups as M
from ...messages.text import admission_channel_text as T
from config.environment_vars import CHANNELS

ADMISSIONS_CHANNEL_ID: int = CHANNELS['admissions']

# Sub router of the parent Router(name="admissions_channel_root")
router = Router(name="admissions_channel_general")


async def post_video(
    message: Message,
    bot: Bot,
    event_from_user: User,
    current_utc_time: datetime,
    channel_id: Union[int, str] = ADMISSIONS_CHANNEL_ID
) -> None:
    caption_data: Dict[str, Any] = T.post_video(message, event_from_user, current_utc_time)

    message = await bot.send_video(
        chat_id=int(channel_id),
        video=message.video.file_id,
        caption=caption_data.get('text'),
        caption_entities=caption_data.get('entities'),
        reply_markup=M.post_video()
    )
    await pin_post(message, bot)


@router.callback_query(F.data.in_({MD.VIDEO_LIKED_DATA, MD.VIDEO_DISLIKED_DATA}))
async def confirm_decision(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    caption_data: Dict[str, Any] = T.confirm_decision(callback_query)

    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=caption_data.get('text'),
        caption_entities=caption_data.get('entities'),
        reply_markup=M.confirm_decision(callback_query.data)
    )


@router.callback_query(
    F.data.in_({MD.CONFIRMED_LIKED_DATA, MD.CONFIRMED_DISLIKED_DATA}),
    flags={AF.I18N_ADMISSIONS: True}
)
async def confirmed_decision(
    callback_query: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
    current_utc_time: datetime
) -> None:
    from ..private_chat.user.general import notify_user_desicion

    caption_data: Dict[str, Any] = T.confirmed_decision(callback_query)

    message = await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=caption_data.get('text'),
        caption_entities=caption_data.get('entities'),
        reply_markup=None
    )

    await unpin_post(message, bot)
    await notify_user_desicion(message, bot, callback_query.data, current_utc_time)


@router.callback_query(F.data == MD.NOT_CONFIRMED_DATA)
async def not_confirmed(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    caption_data: Dict[str, Any] = T.not_confirmed(callback_query)

    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=callback_query.message.message_id,
        caption=caption_data.get('text'),
        caption_entities=caption_data.get('entities'),
        reply_markup=M.post_video()
    )


async def pin_post(message: Message, bot: Bot):
    await bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        disable_notification=True
    )


async def unpin_post(message: Message, bot: Bot):
    await bot.unpin_chat_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )