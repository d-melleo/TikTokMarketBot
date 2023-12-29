"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""

from datetime import datetime
from typing import Any, Dict, List, Union

from aiogram.utils.formatting import as_marked_list, as_list, Code, Bold, Italic
from aiogram.utils.i18n import gettext as _
from pymongo.results import UpdateResult

from . import emojies as emj
from ...enums import PrivateChatRoles, Response
from ...enums import role_commands as cmd
from ...tools.text_formatter import text_formatter
from ..text.private_chat_text import hold_timer
from db.userdata import UserData


def invalid_username() -> str:
    return _(
        "{emj} Invalid username."
    ).format(emj=emj.PROHIBITED)


def not_in_database(subject_username: str) -> str:
    return _(
        "{emj} The user @{subject_username} does not use the bot."
    ).format(emj=emj.PROHIBITED, subject_username=subject_username)


def not_found() -> str:
    return _(
        "{emj} Oops... Something went wrong. Please, try again."
    ).format(emj=emj.DISAPPOINT)


def provide_username(action: str) -> str:
    if action == cmd.Admin.BAN:
        txt = _("{emj} Provide the username you would like to ban.")
    elif action == cmd.Admin.UNBAN:
        txt = _("{emj} Provide the username you would like to unban.")
    elif action == cmd.Admin.HOLD:
        return text_formatter(
            text=_(
                "{emj1} Provide the username you would like to place on hold,"
                +" specifying the duration in hours.\n\n{emj2} For example, {example}."
            ),
            values={
                "emj1": emj.MAGNIFYING_GLASS,
                "emj2": emj.RED_TRIANGLE,
                "example": Italic("john_smith 3")
            }
        )
    elif action == cmd.Admin.RELEASE:
        txt = _("{emj} Provide the username you would like to release from hold.")
    elif action == cmd.Admin.GET:
        txt = _("{emj} Provide the username you would like to get from data base.")
    elif action == cmd.SuperAdmin.ADD_ADMIN:
        txt = _("{emj} Provide the username you would like to promote to administrator.")
    elif action == cmd.SuperAdmin.REMOVE_ADMIN:
        txt = _("{emj} Provide the username you would like to demote from administrator.")
    elif action == cmd.Creator.ADD_SUPERADMIN:
        txt = _("{emj} Provide the username you would like to promote to super admin.")
    elif action == cmd.Creator.REMOVE_SUPERADMIN:
        txt = _("{emj} Provide the username you would like to demote from super admin.")
    else:
        return None
    return txt.format(emj=emj.MAGNIFYING_GLASS)


def cannot_username_yourself(action: str) -> str:
    if action == cmd.Admin.BAN:
        txt = _("{emj} You cannot ban yourself.")
    elif action == cmd.Admin.UNBAN:
        txt = _("{emj} You cannot apply the unban command to yourself.")
    elif action == cmd.Admin.HOLD:
        txt = _("{emj} You cannot put yourself on hold.")
    elif action == cmd.Admin.RELEASE:
        txt = _("{emj} You cannot apply the release command to yourself.")
    elif action == cmd.Admin.GET:
        txt = _("{emj} You cannot retrieve your information from the database by yourself.")
    elif action in [
            cmd.SuperAdmin.ADD_ADMIN,
            cmd.SuperAdmin.REMOVE_ADMIN,
            cmd.Creator.ADD_SUPERADMIN,
            cmd.Creator.REMOVE_SUPERADMIN
            ]:
        txt = _("{emj} You cannot apply this command to yourself.")
    else:
        return None
    return txt.format(emj=emj.PROHIBITED)


def no_permission(action: str, subject_username: str) -> str:
    if action == cmd.Admin.BAN:
        txt = _("{emj} You don't have permission to ban @{subject_username}.")
    elif action == cmd.Admin.UNBAN:
        txt = _("{emj} You don't have permission to unban @{subject_username}.")
    elif action == cmd.Admin.HOLD:
        txt = _("{emj} You don't have permission to put @{subject_username} on hold.")
    elif action == cmd.Admin.RELEASE:
        txt = _("{emj} You don't have permission to release @{subject_username} from hold.")
    elif action == cmd.Admin.GET:
        txt = _("{emj} You don't have permission to retrieve information from the database"
                +" for the user @{subject_username}.")
    elif action == cmd.SuperAdmin.ADD_ADMIN:
        txt = _("{emj} You don't have permission to promote @{subject_username} to administrator.")
    elif action == cmd.SuperAdmin.REMOVE_ADMIN:
        txt = _("{emj} You don't have permission to demote @{subject_username} from administrator.")
    elif action == cmd.Creator.ADD_SUPERADMIN:
        txt = _("{emj} You don't have permission to promote @{subject_username} to super admin.")
    elif action == cmd.Creator.REMOVE_SUPERADMIN:
        txt = _("{emj} You don't have permission to demote @{subject_username} from super admin.")
    else:
        return None
    return txt.format(emj=emj.PROHIBITED, subject_username=subject_username)


def ban(action_response: Response, subject_user: UserData) -> str:
    if action_response == Response.OK:
        return _(
            "{emj} You have successfully banned @{subject_username}."
        ).format(emj=emj.POSITIVE, subject_username=subject_user.username)
    elif action_response == Response.NOT_MODIFIED:
        return _(
            "{emj} @{subject_username} is already banned."
        ).format(emj=emj.EYES, subject_username=subject_user.username)


def unban(action_response: Response, subject_user: UserData) -> str:
    if action_response == Response.OK:
        return _(
            "{emj} You have successfully unbanned @{subject_username}."
        ).format(emj=emj.POSITIVE, subject_username=subject_user.username)
    elif action_response == Response.NOT_MODIFIED:
        return _(
            "{emj} @{subject_username} is not banned."
        ).format(emj=emj.EYES, subject_username=subject_user.username)


def hold(action_response: Response, subject_user: UserData, current_utc_time: datetime) -> str:
    if action_response == Response.OK:
        timer: str = hold_timer(subject_user.hold_timer(current_utc_time))
        return _(
            "{emj} The user @{subject_username} has been placed on hold for{timer}."
        ).format(emj=emj.POSITIVE, subject_username=subject_user.username, timer=timer)


def invalid_hold_command() -> Dict[str, Any]:
    template = _("username hours")
    text = _("{emj1} Invalid format.\nProvide the command as follows: /hold {template}.\n\n{emj2} For example, /hold {example}.")
    values = {
        "emj1": emj.PROHIBITED,
        "emj2": emj.RED_TRIANGLE,
        "template": Italic(template),
        "example": Italic("john_smith 3")
    }
    return text_formatter(text, values)


def release(action_response: Response, subject_user: UserData) -> str:
    if action_response == Response.OK:
        return _(
            "{emj} You have successfully released @{subject_username}."
        ).format(emj=emj.POSITIVE, subject_username=subject_user.username)
    elif action_response == Response.NOT_MODIFIED:
        return _(
            "{emj} The user @{subject_username} is not on hold."
        ).format(emj=emj.EYES, subject_username=subject_user.username)


def release_all(action_response: Response, modified_count: UpdateResult, objects: List[str]) -> Union[str, Dict[str, Any]]:
    if action_response == Response.OK:
        txt = _("{emj} Released {modified_count}/{objects_count} users:\n\n{objects}")
        values = {
            "emj": emj.POSITIVE,
            "modified_count": Bold(modified_count),
            "objects_count": Bold(len(objects)),
            "objects": as_list(*[Bold(x) for x in objects])
        }
        return text_formatter(txt, values)

    elif action_response == Response.NOT_MODIFIED:
        return _(
            "{emj} There are no users to be released."
        ).format(emj=emj.NO_SEE_MONKEY)


def get(action_response: Response, subject_user: UserData) -> Dict[str, Any]:
    if action_response == Response.OK:
        txt = _("{emj} Information retrieved from data base:\n")
        values = {
            "emj": emj.MONKEY,
        }

        for key, value in subject_user.__dict__.items():
            # Manually create placeholders
            txt += '\n{'+str(key)+'}'
            txt += ': {'+str(key)+'_value'+'}'
            # Date&time formatting
            if isinstance(value, datetime):
                value = value.strftime("%d/%m/%Y %H:%M:%S")
            # Key & value formats
            values[key] = Bold(key)
            values[key+'_value'] = Code(value)

        return text_formatter(txt, values)


def ban_list(action_response: Response, objects: List[str]) -> Union[str, Dict[str, Any]]:
    if action_response == Response.OK:
        if objects:
            txt = _("{emj} The list of banned users {objects_count}:\n\n{objects}")
            values = {
                "emj": emj.MONKEY,
                "objects_count": Bold(f"({len(objects)})"),
                "objects": as_list(*[Bold(x) for x in objects])
            }
            return text_formatter(txt, values)
        else:
            return _("{emj} There are no banned users.").format(emj=emj.NO_SEE_MONKEY)


def hold_list(action_response: Response, objects: List[str]) -> Union[str, Dict[str, Any]]:
    if action_response == Response.OK:
        if objects:
            txt = _("{emj} The list of users on hold {objects_count}:\n\n{objects}")
            values = {
                "emj": emj.MONKEY,
                "objects_count": Bold(f"({len(objects)})"),
                "objects": as_list(*[Bold(x) for x in objects])
            }
            return text_formatter(txt, values)
        else:
            return _("{emj} There are no users on hold.").format(emj=emj.NO_SEE_MONKEY)


def add_admin(action_response: Response, subject_user: UserData, pre_role: PrivateChatRoles) -> str:
    role = subject_user.role

    if action_response == Response.OK:
        if role == PrivateChatRoles.ADMIN:
            txt = _("{emj} You have successfully promoted @{subject_username} to administrator.")
        elif role == PrivateChatRoles.SUPERADMIN:
            if pre_role == PrivateChatRoles.ADMIN:
                txt = _("{emj} You have successfully promoted @{subject_username} from admin to super admin.")
            else:
                txt = _("{emj} You have successfully promoted @{subject_username} to super admin.")
        else:
            return None
        return txt.format(emj=emj.POSITIVE, subject_username=subject_user.username)

    elif action_response == Response.NOT_MODIFIED: 
        if role == PrivateChatRoles.ADMIN:
            txt = _("{emj} The user @{subject_username} is already an administrator.")
        elif role == PrivateChatRoles.SUPERADMIN:
            txt = _("{emj} The user @{subject_username} is already a super admin.")
        else:
            return None
        return txt.format(emj=emj.EYES, subject_username=subject_user.username)


def remove_admin(action_response: Response, subject_user: UserData, pre_role: PrivateChatRoles) -> str:
    if action_response == Response.OK:
        if pre_role == PrivateChatRoles.ADMIN:
            txt = _("{emj} You have successfully demoted @{subject_username} from administrator.")
        elif pre_role == PrivateChatRoles.SUPERADMIN:
            txt = _("{emj} You have successfully demoted @{subject_username} from super admin.")
        else:
            return None
        return txt.format(emj=emj.POSITIVE, subject_username=subject_user.username)

    elif action_response == Response.NOT_MODIFIED:
        if pre_role == PrivateChatRoles.USER:
            txt = _("{emj} The user @{subject_username} is not an administrator.")
        elif pre_role == PrivateChatRoles.SUPERADMIN:
            txt = _(
                "{emj} The user @{subject_username} is a super admin. "
                +"You must use the /remove_superadmin command instead."
            )
        else:
            return None
        return txt.format(emj=emj.PROHIBITED, subject_username=subject_user.username)