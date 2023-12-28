from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ....enums import PrivateChatRoles, Response
from ....enums.role_commands import SuperAdmin
from ....messages.text import private_chat_admin as T
from ....states import AdminCommand
from ....tools.admin_commands import resolve_response
from ....tools.router_setup import register_filters
from db.userdata import DBConnect, UserData


# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_superadmin")

filters = {
    MagicData(F.my_user.role.in_({
        PrivateChatRoles.SUPERADMIN,
        PrivateChatRoles.CREATOR
    })),
    Command(*list(SuperAdmin))
}
# Register filters for this sub router.
register_filters(router, filters)

# Check if a command if followed by a value
pattern = r"^/\w+\ +\@?\w+$"


@router.message(Command(SuperAdmin.ADD_ADMIN), F.text.regexp(pattern))
@resolve_response
async def add_admin(message: Message, subject_user: UserData, **data):
    if subject_user.role in [
        PrivateChatRoles.ADMIN,
        PrivateChatRoles.SUPERADMIN
    ]:
        # User is already an administrator
        action_response = Response.NOT_MODIFIED
    else:
        # Update the role
        action_response = await DBConnect.collection.update_one(
            {'_id': subject_user._id},
            {'$set': {'role': PrivateChatRoles.ADMIN}}
        )
        action_response = action_response.raw_result['updatedExisting']
        subject_user.role = PrivateChatRoles.ADMIN
    return {
        "action_response": action_response,
        "reply_text_resolver": T.add_admin
    }



@router.message(Command(SuperAdmin.REMOVE_ADMIN), F.text.regexp(pattern))
@resolve_response
async def remove_admin(message: Message, subject_user: UserData, **data):
    pre_role = subject_user.role
    if subject_user.role == PrivateChatRoles.ADMIN:
        # Update the role
        action_response = await DBConnect.collection.update_one(
            {'_id': subject_user._id},
            {'$set': {'role': PrivateChatRoles.USER}}
        )
        action_response = action_response.raw_result['updatedExisting']
        subject_user.role = PrivateChatRoles.USER
    else:
        action_response = Response.NOT_MODIFIED
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda *args: T.remove_admin(pre_role=pre_role, *args)
    }


@router.message(Command(*list(SuperAdmin)), ~F.text.regexp(pattern))
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