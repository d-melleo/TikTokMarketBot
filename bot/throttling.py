from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from cachetools import TTLCache

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import Chat, Update
from aiogram.enums.chat_type import ChatType

from config import CHANNELS


CHANNELS: Dict[str, int]
CURRENT_UTC_TIME_KEY = "current_utc_time"
EVENT_CHAT_KEY = "event_chat"


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.CACHE_FLAG = 'cached'
        self.cache = TTLCache(maxsize=10_000, ttl=0.75) # time to live = 1 sec

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        print("THROTTLING IN")

        event_chat: Chat = data[EVENT_CHAT_KEY]

        if event_chat.type == ChatType.CHANNEL and \
                event_chat.id not in CHANNELS.values():
            return

        # Skip the handling if a user is spamming
        if event_chat.type == ChatType.PRIVATE and \
                event_chat.id in self.cache:
            return

        if event_chat.type == ChatType.PRIVATE:
            # Cache a user for 0.75 sec
            self.cache[event_chat.id] = self.CACHE_FLAG

        # Pass current date&time
        data[CURRENT_UTC_TIME_KEY] = datetime.utcnow()

        # Execute handler
        await handler(event, data)

        print("THROTTLING OUT")