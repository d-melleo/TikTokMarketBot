from enum import Enum


class PrivateChatRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    CREATOR = "creator"