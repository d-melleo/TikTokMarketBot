from typing import Set

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, MagicData

router = Router(name="private_general")

_filters: Set[MagicData] = {
    MagicData(~F.my_user.is_banned)
}

_exclude = ["update", "error"]
for observer_name, observer_event in router.observers.items():
    if observer_name not in _exclude:
        observer_event.filter(*_filters)


@router.message()
async def start(message: Message) -> None:
    await message.reply(text='Hello PRIVATE!')


@router.callback_query()
async def query(callback_query: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Callback PRIVATE!')