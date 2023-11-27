from enum import Enum


class MyRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    CREATOR = "creator"