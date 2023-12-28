from aiogram import Bot, F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message

from ....enums import PrivateChatRoles
from ....enums.role_commands import Creator
from ....tools.router_setup import register_filters

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_creator")

filters = {
    MagicData(F.my_user.role == PrivateChatRoles.CREATOR),
    Command(*list(Creator))
}
# Register filters for this sub router.
register_filters(router, filters)

# Check if a command if followed by a value
pattern = r"^/\w+\ +\w+$"


@router.message(Command(Creator.ADD_SUPERADMIN), F.text.regexp(pattern))
async def add_superadmin(message: Message, bot: Bot):
    print("ADMIN", True, message.text)


@router.message(Command(Creator.REMOVE_SUPERADMIN), F.text.regexp(pattern))
async def remove_superadmin(message: Message, bot: Bot):
    print("ADMIN", True, message.text)