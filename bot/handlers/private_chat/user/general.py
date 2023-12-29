from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command, MagicData
from aiogram.types import CallbackQuery, Chat, Message, User

from ....messages.markups import private_chat_markup as M
from ....messages.text import private_chat_text as T
from ....enums import PrivateChatMarkupData as MD
from ....enums.role_commands import User
from bot.tools.router_setup import register_filters
from bot.tools.get_mentioned_user import get_mentioned_user
from db.userdata import UserData, get_my_user

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_general")

filters = {
    MagicData(~F.my_user.is_banned),
    (MagicData(F.current_utc_time > F.my_user.hold_until))
}
# Register filters for this sub router.
register_filters(router, filters)


@router.message(Command(User.START))
async def start(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.start(),
        reply_markup=M.send_video()
    )


@router.message(Command(User.HELP))
async def help(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.help(),
        reply_markup=M.send_video()
    )


@router.message(Command(User.LANGUAGE))
async def language(message: Message, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.language(),
        reply_markup=M.language()
    )


@router.callback_query(F.data.in_({
    MD.EN_LANGUAGE_DATA, MD.PL_LANGUAGE_DATA, MD.UK_LANGUAGE_DATA
}))
async def set_language(callback_query: CallbackQuery, bot: Bot, event_chat: Chat, my_user: UserData):
    await my_user.set_language(callback_query.data)

    await bot.send_message(
        chat_id=event_chat.id,
        text=T.set_language(callback_query.data)
    )


@router.callback_query(F.data == MD.SEND_VIDEO_DATA)
async def request_video(callback_query: CallbackQuery, bot: Bot, event_chat: Chat):
    await bot.send_message(
        chat_id=event_chat.id,
        text=T.request_video()
    )


@router.message((F.video.duration <= 62) & (~F.media_group_id))
async def received_video(
    message: Message, bot: Bot, event_chat: Chat,
    event_from_user: User, my_user: UserData,
    current_utc_time: datetime
) -> None:
    from ...admission_channel.general import post_video

    # Send a video to the Admissions channel
    await post_video(message, bot, event_from_user, current_utc_time)

    # Set a user on hold for 4 hours, user won't be able to send new videos
    await my_user.hold(current_utc_time, hrs=3)

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


async def notify_user_desicion(
    message: Message,
    bot: Bot,
    decision: str,
    current_utc_time: datetime
) -> None:
    # Mentioned use is the user who's sent a video
    video_from_user: User = get_mentioned_user(message)

    await bot.send_message(
        chat_id=video_from_user.id,
        text=T.notify_user_desicion(decision),
        reply_markup=M.send_video()
    )

    # Allow user to send videos again
    subject_user: UserData = await get_my_user(video_from_user, current_utc_time)
    await subject_user.release(current_utc_time)