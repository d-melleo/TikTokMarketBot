from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware, Bot
from aiogram.types import BotCommand, Message, TelegramObject
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from ..messages.private_chat_commands_menu import get_my_commands
from db.userdata import UserData


class CommandsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
        ) -> Any:
        print("COMMANDS IN")

        # Retrieve the bot instance from the data dictionary.
        bot: Bot = data['bot']

        # Retrieve the user's instance passed from the outer DatabaseMiddleware.
        my_user: UserData = data['my_user']

        # Set the commands for the user based on their role.
        my_user.commands: List[BotCommand] = get_my_commands(my_user)

        # Set the commands available for the user in the bot.
        await bot.set_my_commands(
            commands=my_user.commands,
            scope=BotCommandScopeChat(chat_id=my_user._id))
        
        # Execute the handler.
        await handler(event, data)

        print("COMMANDS OUT")