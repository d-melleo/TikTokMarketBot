from aiogram import Bot, Router
from aiogram.types import Chat, CallbackQuery, Message


router = Router(name="admissions_general")


@router.channel_post()
async def start(message: Message) -> None:
    await message.reply(text='Message CHANNEL!')


@router.callback_query()
async def query(callback_query: CallbackQuery, bot: Bot, event_chat: Chat) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text="CHANNEL CALLBACK!!!"
    )