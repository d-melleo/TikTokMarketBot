from typing import List

from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _

from ..enums import commands, PrivateChatRoles
from db.userdata import UserData


class UserCommands:
    def __init__(self) -> None:
        self.START = BotCommand(command=commands.User.START, description=_("Start"))
        self.HELP = BotCommand(command=commands.User.HELP, description=_("Help"))
        self.LANGUAGE = BotCommand(command=commands.User.LANGUAGE, description=_("Language"))


class AdminCommands(UserCommands):
    def __init__(self) -> None:
        super().__init__()

        self.BAN = BotCommand(command=commands.Admin.BAN, description=_("Ban a user"))
        self.UNBAN = BotCommand(command=commands.Admin.UNBAN, description=_("Unban a user"))
        self.HOLD = BotCommand(command=commands.Admin.HOLD, description=_("Prevent a user from sending videos"))
        self.RELEASE = BotCommand(command=commands.Admin.RELEASE, description=_("Allow a user to send videos"))
        self.GET_USER = BotCommand(command=commands.Admin.GET_USER, description=_("Get user's data from DB"))
        self.BAN_LIST = BotCommand(command=commands.Admin.BAN_LIST, description=_("Show banned users"))
        self.HOLD_LIST = BotCommand(command=commands.Admin.HOLD_LIST, description=_("Show users on hold"))


class SuperAdminCommands(AdminCommands):
    def __init__(self) -> None:
        super().__init__()

        self.ADD_ADMIN = BotCommand(command=commands.SuperAdmin.ADD_ADMIN, description=_("Add a new admin"))
        self.REMOVE_ADMIN = BotCommand(command=commands.SuperAdmin.REMOVE_ADMIN, description=_("Remove an admin"))


class CreatorCommands(SuperAdminCommands):
    def __init__(self) -> None:
        super().__init__()

        self.ADD_SUPERADMIN = BotCommand(command=commands.Creator.ADD_SUPERADMIN, description=_("Add a new superadmin"))
        self.REMOVE_SUPERADMIN = BotCommand(command=commands.Creator.REMOVE_SUPERADMIN, description=_("Remove a superadmin"))


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