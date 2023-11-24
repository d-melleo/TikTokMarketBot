from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, Router
from aiogram.enums.chat_type import ChatType
from aiogram.types import TelegramObject, User, Chat

from db.userdata import UserData


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
        event_chat: Chat = data[EVENT_CHAT_KEY]

        if event_chat.type == ChatType.PRIVATE:
            print("DATABASE IN")
            current_utc_time: datetime = data[CURRENT_UTC_TIME_KEY]
            event_from_user: User = data[EVENT_FROM_USER_KEY]

            # Get a user from database
            db_user: Union[Dict[str, Any], None] = await UserData.read_user(event_from_user.id)

            # Write user into DB, and return dict
            if db_user:
                # Check if username or name has changed
                db_user: Dict[str, Any] = await UserData.validate_name(db_user, event_from_user)
                db_user: Dict[str, Any] = await UserData.validate_username(db_user, event_from_user)
                my_user = UserData(db_user)
            else:
                my_user: UserData = await UserData.write_user(event_from_user, current_utc_time)

            # Pass the user's instance into the handler
            data['my_user'] = my_user

            # Execute handler
            await handler(event, data)

            # Update last activity
            await my_user.update_last_activity(current_utc_time)
            print("DATABASE OUT")

        else:
            return await handler(event, data)