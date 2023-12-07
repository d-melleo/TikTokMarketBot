from enum import Enum


class PrivateChatRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    CREATOR = "creator"

    @staticmethod
    def superiority(role1, role2) -> bool:
        role_hierarchy = list(PrivateChatRoles)
        if role1 in role_hierarchy and role2 in role_hierarchy:
            return role_hierarchy.index(role1) > role_hierarchy.index(role2)