from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, Router
from aiogram.enums.chat_type import ChatType
from aiogram.types import Chat, TelegramObject, User

from db.userdata import UserData, get_my_user

CURRENT_UTC_TIME_KEY = "current_utc_time"
EVENT_CHAT_KEY = "event_chat"
EVENT_FROM_USER_KEY = "event_from_user"


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Extract necessary data from the 'data' dictionary.
        current_utc_time: datetime = data[CURRENT_UTC_TIME_KEY]
        event_chat: Chat = data[EVENT_CHAT_KEY]

        # Check if the event is from a private chat.
        if event_chat.type == ChatType.PRIVATE:
            print("DATABASE IN")

            # Retrieve the Telegram user instance from the 'data' dictionary.
            tg_user: User = data[EVENT_FROM_USER_KEY]

            # Retrieve or create a UserData instance for the Telegram user.
            my_user: UserData = await get_my_user(
                tg_user=tg_user,
                current_utc_time=current_utc_time
            )

            # Pass the user's instance into the handler.
            data['my_user'] = my_user

            # Execute the handler.
            await handler(event, data)

            # Update the last activity timestamp.
            await my_user.update_last_activity(current_utc_time)

            print("DATABASE OUT")

        else:
            # For non-private chats, directly invoke the handler
            # without additional processing.
            return await handler(event, data)