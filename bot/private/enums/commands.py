from typing import List

from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _


ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLE_SUPERADMIN = "superadmin"
ROLE_CREATOR = "creator"



class MyCommands:
    def __init__(self, role: str) -> None:
        if role == ROLE_USER:
            self.commands = UserCommands()
        elif role == ROLE_ADMIN:
            self.commands = AdminCommands()
        elif role == ROLE_SUPERADMIN:
            self.commands = SuperAdminCommands()
        elif role == ROLE_CREATOR:
            self.commands = CreatorCommands()

    def __call__(self) -> List[BotCommand]:
        commands: List[BotCommand] = [value\
            for value in vars(self.commands).values()\
                if isinstance(value, BotCommand)
        ]
        return commands


class UserCommands:
    def __init__(self) -> None:
        self.start = BotCommand(command='start', description=_('Start'))
        self.language = BotCommand(command='language', description=_('Language'))
        self.help = BotCommand(command='help', description=_('Help'))


class AdminCommands(UserCommands):
    def __init__(self) -> None:
        super().__init__()
        self.ban = BotCommand(command='ban', description=_('Ban a user'))
        self.unban = BotCommand(command='unban', description=_('Unban a user'))
        self.hold = BotCommand(command='hold', description=_('Prevent a user from sending videos'))
        self.release = BotCommand(command='release', description=_('Allow a user to send videos'))
        self.database = BotCommand(command='database', description=_('Get user\'s data from DB'))
        self.ban_list = BotCommand(command='ban_list', description=_('Show banned users'))
        self.hold_list = BotCommand(command='hold_list', description=_('Show users on hold'))


class SuperAdminCommands(AdminCommands):
    def __init__(self) -> None:
        super().__init__()
        self.add_admin = BotCommand(command='add_admin', description=_('Add a new admin'))
        self.remove_admin = BotCommand(command='remove_admin', description=_('Remove an admin'))


class CreatorCommands(SuperAdminCommands):
    def __init__(self) -> None:
        super().__init__()
        self.add_superadmin = BotCommand(command='add_superadmin', description=_('Add a new superadmin'))
        self.remove_superadmin = BotCommand(command='remove_superadmin', description=_('Remove a superadmin'))

