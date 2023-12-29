from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message

from ....enums import PrivateChatRoles, Response
from ....enums.role_commands import Creator
from ....messages.text import private_chat_admin as T
from ....tools.admin_commands import PATTERN, register_commands_filters, resolve_response
from ....tools.router_setup import register_filters
from db.userdata import DBConnect, UserData

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_creator")

filters = {
    MagicData(F.my_user.role == PrivateChatRoles.CREATOR)
}

# Register filters for this sub router.
register_filters(router, filters)
# Register additional handlers for commands
register_commands_filters(router, F.func(lambda x: globals()).as_("executable"))


@router.message(Command(Creator.ADD_SUPERADMIN), F.text.regexp(PATTERN))
@resolve_response
async def add_superadmin(message: Message, subject_user: UserData, **data):
    pre_role = subject_user.role

    if subject_user.role == PrivateChatRoles.SUPERADMIN:
        # User is already a super admin
        action_response = Response.NOT_MODIFIED
    else:
        # Update the role
        action_response = await DBConnect.collection.update_one(
            {'_id': subject_user._id},
            {'$set': {'role': PrivateChatRoles.SUPERADMIN}}
        )
        action_response = action_response.raw_result['updatedExisting']
        subject_user.role = PrivateChatRoles.SUPERADMIN
    return {
        "action_response": action_response,
        "reply_text_resolver": lambda *args: T.add_admin(pre_role=pre_role, *args)
    }


@router.message(Command(Creator.REMOVE_SUPERADMIN), F.text.regexp(PATTERN))
@resolve_response 
async def remove_superadmin(message: Message, subject_user: UserData, **data):
    pre_role = subject_user.role

    if subject_user.role == PrivateChatRoles.SUPERADMIN:
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