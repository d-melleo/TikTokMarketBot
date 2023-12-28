from aiogram import F, Router
from aiogram.filters import Command, CommandObject, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ....enums import PrivateChatRoles, Response
from ....enums.role_commands import Admin
from ....messages.text import private_chat_admin as T
from ....states import AdminCommand
from ....tools.admin_commands import resolve_response
from ....tools.router_setup import register_filters
from db.userdata import DBConnect, UserData

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_admin")

filters = {
    MagicData(F.my_user.role.in_({
        PrivateChatRoles.ADMIN,
        PrivateChatRoles.SUPERADMIN,
        PrivateChatRoles.CREATOR
    }))
}
# Register filters for this sub router.
register_filters(router, filters)

# Check if a command if followed by a value
pattern = r"^/\w+\ +\@?\w+$"


@router.message(Command(Admin.BAN), F.text.regexp(pattern))
@resolve_response
async def ban(message: Message, subject_user: UserData, **data):
    if subject_user.is_banned:
        # User is already banned
        action_response = Response.NOT_MODIFIED
    else:
        # Attempt to ban a user
        action_response = await subject_user.ban()
    # Return the response code or bool if not code and text function
    return {
        "action_response": action_response,
        "reply_text_resolver": T.ban
    }


@router.message(Command(Admin.UNBAN), F.text.regexp(pattern))
@resolve_response
async def unban(message: Message, subject_user: UserData, **data):
    if not subject_user.is_banned:
        # User isn't banned
        action_response = Response.NOT_MODIFIED
    else:
        # Attempt to unban a user
        action_response = await subject_user.unban()
    # Return the response code or bool if not code and text function
    return {
        "action_response": action_response,
        "reply_text_resolver": T.unban
    }


@router.message(Command(Admin.HOLD), F.text.regexp(r"^/\w+\ +\@?\w+\ *\d*$"))
@resolve_response
async def hold(message: Message, subject_user: UserData, hold_for: int, current_utc_time, **data):
    # Put the user on hold
    action_response = await subject_user.hold(current_utc_time, hrs=hold_for)
    # Return the response code or bool if not code and text function
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda *args: T.hold(current_utc_time=current_utc_time, *args)
    }


@router.message(Command(Admin.RELEASE), F.text.regexp(pattern))
@resolve_response
async def release(message: Message, subject_user: UserData, current_utc_time, **data):
    if subject_user.hold_until < current_utc_time:
        # The user is not hold
        action_response = Response.NOT_MODIFIED
    else:
        # Attempt to release the user
        action_response = await subject_user.release(current_utc_time)
    # Return the response code or bool if not code and text function
    return {
        "action_response": action_response,
        "reply_text_resolver": T.release
    }


@router.message(
    Command(Admin.RELEASE_ALL),
    F.text == f"/{Admin.RELEASE_ALL.value}",
    flags={'subject_user': 'bypass'}
)
@resolve_response
async def release_all(message: Message, current_utc_time, **data):
    # Get the list of users to be released
    objects = DBConnect.collection.find(
        {'hold_until': {'$gte': current_utc_time}}
    )
    objects = ["@"+x.get("username") async for x in objects]

    # Release the users
    if objects:
        result = await DBConnect.collection.update_many(
            {'hold_until': {'$gte': current_utc_time}},
            {'$set': {'hold_until': current_utc_time}}
        )
        action_response = result.raw_result['updatedExisting']
        modified_count = result.modified_count
    else:
        # No users have been released
        action_response = Response.NOT_MODIFIED
        modified_count = None
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda action_response: T.release_all(action_response, modified_count, objects)
    }


@router.message(Command(Admin.GET), F.text.regexp(pattern))
@resolve_response
async def get(message: Message, **data):
    # Retrieve user's information from database
    # This will actually return the dict of UserData instance
    return {
        "action_response": Response.OK,
        "reply_text_resolver": T.get
    }


@router.message(
    Command(Admin.BAN_LIST),
    F.text == f"/{Admin.BAN_LIST.value}",
    flags={'subject_user': 'bypass'}
)
@resolve_response
async def ban_list(message: Message, **data):
    # Get the list of banned users
    objects = DBConnect.collection.find(
        {'is_banned': True}
    )
    objects = ["@"+x.get("username") async for x in objects]

    # The response is always OK regardless the result
    action_response = Response.OK
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda action_response: T.ban_list(action_response, objects)
    }


@router.message(
    Command(Admin.HOLD_LIST),
    F.text == f"/{Admin.HOLD_LIST.value}",
    flags={'subject_user': 'bypass'}
)
@resolve_response
async def hold_list(message: Message, current_utc_time, **data):
    objects = DBConnect.collection.find(
        {'hold_until': {'$gte': current_utc_time}}
    )
    objects = ["@"+x.get("username") async for x in objects]

    # The response is always OK regardless the result
    action_response = Response.OK
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda action_response: T.hold_list(action_response, objects)
    }


@router.message(
    Command(*list(Admin)),
    ~F.text.regexp(pattern),
    MagicData(F.command.command.not_in({Admin.RELEASE_ALL, Admin.BAN_LIST, Admin.HOLD_LIST}))
)
async def incomplete_command(message: Message, state: FSMContext, command: CommandObject):
    # Set FSM state to await for a username input
    await state.set_state(AdminCommand.incomplete_command)
    # Store function to be execute for the provided command
    await state.update_data(executable=globals().get(command.command))


@router.message(AdminCommand.incomplete_command, F.text)
async def complete_command(message: Message, **data):
    state = data["state"]
    state_data = await state.get_data()  # State's storage data
    await state.clear()  # Finish state' conversation
    executable = state_data.get("executable")  # Function to be executed

    # Execute the handler
    if executable:
        return await executable(message, **data)