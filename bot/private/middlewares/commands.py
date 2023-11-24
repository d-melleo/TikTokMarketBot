from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware, Bot
from aiogram.types import BotCommand, Message, TelegramObject
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from ..enums.commands import MyCommands
from db.userdata import UserData



class CommandsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        print("COMMANDS IN")

        # Get the bot instance from data
        bot: Bot = data['bot']

        # Get user's instance that hasa been passed from the outer DatabaseMiddleware
        my_user: UserData = data['my_user']
        # Set the commands for the user based on user's role
        my_user.commands: List[BotCommand] = MyCommands(my_user.role)()

        # Set commands available for the user in the bot
        await bot.set_my_commands(
            commands=my_user.commands,
            scope=BotCommandScopeChat(chat_id=my_user._id))

        # Execute handler
        await handler(event, data)

        print("COMMANDS OUT")