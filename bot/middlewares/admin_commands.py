from datetime import datetime
import re
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

from ..enums import PrivateChatRoles, Response
from ..enums.role_commands import Admin
from ..messages.text import private_chat_admin as T
from db.userdata import DBConnect, UserData


class AdminCommands(BaseMiddleware):
    def __init__(self) -> None:
        self.action: str = None
        self.admin_user: UserData = None
        self.subject_user: UserData = None
        self.subject_username: str = None
        self.reply_text: str = None
        self.data: Dict[str, Any] = None

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
        ) -> Any:
        self.__init__()  # Reset class's variables upon each call

        self.data = data
        self.action = await self.resolve_action()  # Get trigerred command's name
        self.admin_user = self.data.get("my_user")  # Admin user initiated the command
        # Get provided username from text message
        self.subject_username = self.resolve_subject_username(event)

        if self.subject_username:
            if not self.is_username_myself():
                subject_user = await self.is_username_in_database()
                if subject_user:
                    if self.is_permission(subject_user):
                        self.subject_user = subject_user

        self.data.update(
            reply_text=self.reply_text,
            subject_user=self.subject_user
        )

        # Execute the handler.
        respose_data = await handler(event, self.data)

        # Reply with a completion status
        await self.data["bot"].send_message(
            chat_id=event.chat.id,
            **self.resolve_reply_text(respose_data)
        )

    async def resolve_action(self) -> str:
        state_data = await self.data.get("state").get_data()
        action = state_data.get("executable") or self.data.get("command")

        if callable(action):
            return action.__wrapped__.__name__
        elif isinstance(action, CommandObject):
            return action.command

    def resolve_subject_username(self, event: Message) -> str:
        # Get text from the message
        subject_username = event.text
        # Remove command from the text
        subject_username = re.sub(f"/{self.action}", "", subject_username)
        # Remove the @ sign from the username
        subject_username = re.sub("@", "", subject_username)
        # Remove extra whitespaces and blank lines
        subject_username = subject_username.strip("\n").strip()

        if not subject_username:
            # Username is an empty string
            self.reply_text = T.provide_username(self.action)
        else:
            # For /hold command expected input [/hold username hrs], e.g. /hold john_smith 3
            hold_command_pattern = re.fullmatch(r"^\@?\w+\ +\d+$", subject_username)
            if self.action == Admin.HOLD and hold_command_pattern:
                # Separate the username and hours to be put on hold for
                subject_username, hold_for = subject_username.split()
                self.data.update(hold_for=int(hold_for))
            elif self.action == Admin.HOLD and not hold_command_pattern:
                subject_username = None
                self.reply_text = T.invalid_hold_command()
            # General username validation
            elif not re.fullmatch(r"\w+", subject_username):
                subject_username = None
                self.reply_text = T.invalid_username()

        return subject_username

    def resolve_reply_text(self, respose_data: Dict[str, Any]) -> Dict[str, Any]:
        action_response = Response.CONTINUE

        if respose_data:
            # response_data returned by the handler if executed
            action_response = respose_data.get("action_response")

        if action_response in [Response.OK, Response.NOT_MODIFIED]:
            # Text specific to each command, defined in the hanler
            reply_text = respose_data.get("reply_text")
        elif action_response == Response.NOT_FOUND:
            # Pre-defined text on False response from DB
            reply_text = T.not_found()
        elif action_response == Response.CONTINUE:
            # Pre-defined text before the handler's execution
            reply_text = self.reply_text

        if not isinstance(reply_text, dict):
            # 1. reply_text with entities (Bold, Italic, ect.) returns a dict with keys: 'text' and 'entities'
            # 2. reply_text with a plain text returns only a string,
                # in this case it must be returned as a dict with a 'text' key
            reply_text = {"text": reply_text}
        return reply_text

    def is_username_myself(self) -> bool:
        myself = self.admin_user.username == self.subject_username
        if myself:
            self.reply_text = T.cannot_username_yourself(self.action)
        return myself

    async def is_username_in_database(self) -> UserData:
        subject_user = await DBConnect.collection.find_one(
            {"username": self.subject_username}
        )
        if not subject_user:
            self.reply_text = T.not_in_database(self.subject_username)
        else:
            subject_user = UserData(subject_user, self.data.get("current_utc_time"))
        return subject_user

    def is_permission(self, subject_user: UserData) -> bool:
        permission_ = PrivateChatRoles.superiority(
            self.admin_user.role,
            subject_user.role
        )
        if not permission_:
            self.reply_text = T.no_permission(self.action, self.subject_username)
        return permission_
