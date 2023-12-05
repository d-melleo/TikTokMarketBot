from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums.chat_type import ChatType
from aiogram.types import TelegramObject
from aiogram.types import Chat, Update
from cachetools import TTLCache

from config.environment_vars import CHANNELS

CHANNELS: Dict[str, int]
CURRENT_UTC_TIME_KEY = "current_utc_time"
EVENT_CHAT_KEY = "event_chat"


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.CACHE_FLAG = 'cached'
        self.cache = TTLCache(maxsize=10_000, ttl=0.75)  # Time to live (ttl) in cache is 0.75s.

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        event_chat: Chat = data[EVENT_CHAT_KEY]

        # Execute a handler only for my channels.
        if event_chat.type == ChatType.CHANNEL and \
                event_chat.id not in CHANNELS.values():
            return

        # Skip the handling if a user is spamming.
        if event_chat.type == ChatType.PRIVATE and \
                event_chat.id in self.cache:
            return

        # Cache a user for 0.75s to sprevent spam.
        if event_chat.type == ChatType.PRIVATE:
            # Cache a user for 0.75 sec
            self.cache[event_chat.id] = self.CACHE_FLAG

        # Pass current date&time to the handler.
        data[CURRENT_UTC_TIME_KEY] = datetime.utcnow()

        # Execute handler.
        return await handler(event, data)