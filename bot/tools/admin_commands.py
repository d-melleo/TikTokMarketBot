import functools
from typing import List, Type

from aiogram import F, Router
from aiogram.dispatcher.flags import get_flag
from aiogram.filters import Command, CommandObject, Filter, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..enums import Response
from ..enums.role_commands import Admin, SuperAdmin, Creator
from ..states import AdminCommand
from db.userdata import UserData

# Check if a command if followed by a username
# Username can be either with or without the '@' sign
PATTERN = r"^/\w+\ +\@?\w+$"


def resolve_response(func):
    def response_code(action_response) -> Response:
        if not isinstance(action_response, Response):
            if action_response:
                action_response = Response.OK
            else:
                action_response = Response.NOT_FOUND
        return action_response

    @functools.wraps(func)
    async def wrapper(message, **data):
        subject_user: UserData = data.get("subject_user")

        if subject_user or (get_flag(data, "subject_user") == "bypass"):
            # Execute the handler and unpack variables
            action_response, reply_text_resolver = (await func(message, **data)).values()
            # Resolve the response code
            action_response = response_code(action_response)
            # reply_text will be passed to the 'admin_command.py' middleware
            if subject_user:
                reply_text = reply_text_resolver(action_response, subject_user)
            else:
                reply_text = reply_text_resolver(action_response)
        else:
            action_response = Response.CONTINUE
            reply_text = None

        return {
            "action_response": action_response,
            "reply_text": reply_text
        }
    return wrapper


async def incomplete_command(
    message: Message, state: FSMContext, command: CommandObject, executable
) -> None:
    # Set FSM state to await for a username input
    await state.set_state(AdminCommand.incomplete_command)
    # Store function to be execute for the provided command
    await state.update_data(executable=executable.get(command.command))


async def complete_command(message: Message, **data) -> None:
    state = data["state"]
    state_data = await state.get_data()  # State's storage data
    await state.clear()  # Finish state' conversation
    executable = state_data.get("executable")  # Function to be executed

    # Execute the handler
    if executable:
        return await executable(message, **data)


def _role_commands(router: Router) -> List[Type[Filter]]:
    filters = []

    if router.name == "private_chat_admin":
        filters.append(Command(*list(Admin)))
        # Exclude command, that do not require a username
        filters.append(
            MagicData(F.command.command.not_in({
                Admin.RELEASE_ALL, Admin.BAN_LIST, Admin.HOLD_LIST
            }))
        )
    elif router.name == "private_chat_superadmin":
        filters.append(Command(*list(SuperAdmin)))
    elif router.name == "private_chat_creator":
        filters.append(Command(*list(Creator)))

    return filters


def register_commands_filters(router: Router, router_global_vars) -> None:
    # Registers a handler for incomplete commands. Commands, that are missing a username
    router.message.register(
        incomplete_command,
        router_global_vars,
        ~F.text.regexp(PATTERN),
        *_role_commands(router)
    )

    # Register handler that receives a username in a second message after the command
    router.message.register(
        complete_command,
        AdminCommand.incomplete_command,
        (F.text.regexp(r"^\@?\w+$") | F.text.regexp(PATTERN))
    )
