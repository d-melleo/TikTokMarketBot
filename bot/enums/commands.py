from enum import Enum


class User(str, Enum):
    START = "start"
    HELP = "help"
    LANGUAGE = "language"


class Admin(str, Enum):
    BAN = "ban"
    UNBAN = "unban"
    HOLD = "hold"
    RELEASE = "release"
    GET_USER = "get_user"
    BAN_LIST = "ban_list"
    HOLD_LIST = "hold_list"


class SuperAdmin(str, Enum):
    ADD_ADMIN = "add_admin"
    REMOVE_ADMIN = "remove_admin"


class Creator(str, Enum):
    ADD_SUPERADMIN = "add_superadmin"
    REMOVE_SUPERADMIN = "remove_superadmin"