from typing import List

from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _

from ..enums.private_chat_roles import PrivateChatRoles
from db.userdata import UserData


class UserCommands:
    def __init__(self) -> None:
        self.START = BotCommand(command="start", description=_("Start"))
        self.HELP = BotCommand(command="help", description=_("Help"))
        self.LANGUAGE = BotCommand(command="language", description=_("Language"))


class AdminCommands(UserCommands):
    def __init__(self) -> None:
        super().__init__()

        self.BAN = BotCommand(command="ban", description=_("Ban a user"))
        self.UNBAN = BotCommand(command="unban", description=_("Unban a user"))
        self.HOLD = BotCommand(command="hold", description=_("Prevent a user from sending videos"))
        self.RELEASE = BotCommand(command="release", description=_("Allow a user to send videos"))
        self.GET_USER = BotCommand(command="get_user", description=_("Get user's data from DB"))
        self.BAN_LIST = BotCommand(command="ban_list", description=_("Show banned users"))
        self.HOLD_LIST = BotCommand(command="hold_list", description=_("Show users on hold"))


class SuperAdminCommands(AdminCommands):
    def __init__(self) -> None:
        super().__init__()

        self.ADD_ADMIN = BotCommand(command="add_admin", description=_("Add a new admin"))
        self.REMOVE_ADMIN = BotCommand(command="remove_admin", description=_("Remove an admin"))


class CreatorCommands(SuperAdminCommands):
    def __init__(self) -> None:
        super().__init__()

        self.ADD_SUPERADMIN = BotCommand(command="add_superadmin", description=_("Add a new superadmin"))
        self.REMOVE_SUPERADMIN = BotCommand(command="remove_superadmin", description=_("Remove a superadmin"))


def get_my_commands(my_user: UserData) -> List[BotCommand]:
    if my_user.role == PrivateChatRoles.USER:
        role_commands = UserCommands()
    elif my_user.role == PrivateChatRoles.ADMIN:
        role_commands = AdminCommands()
    elif my_user.role == PrivateChatRoles.SUPERADMIN:
        role_commands = SuperAdminCommands()
    elif my_user.role == PrivateChatRoles.CREATOR:
        role_commands = CreatorCommands()

    # Get commands for a specific role.
    commands = [value for value in vars(role_commands).values() if isinstance(value, BotCommand)]

    return commands