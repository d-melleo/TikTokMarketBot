from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware, Bot
from aiogram.types import BotCommand, Message, TelegramObject
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from ..messages.private_chat_commands_menu import get_my_commands
from db.userdata import UserData


class MenuCommandsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
        ) -> Any:
        # Retrieve the bot instance from the data dictionary.
        bot: Bot = data['bot']

        # Retrieve the user's instance passed from the outer DatabaseMiddleware.
        my_user: UserData = data['my_user']

        # Set the commands available for the user in the bot.
        await bot.set_my_commands(
            commands=get_my_commands(my_user),
            scope=BotCommandScopeChat(chat_id=my_user._id))
        
        # Execute the handler.
        return await handler(event, data)