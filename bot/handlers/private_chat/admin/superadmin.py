from aiogram import Bot, F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message

from ....enums import commands, PrivateChatRoles
from ....tools.router_setup import register_filters

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_superadmin")

filters = {
    MagicData(F.my_user.role.in_({
        PrivateChatRoles.SUPERADMIN,
        PrivateChatRoles.CREATOR
    })),
    Command(*list(commands.SuperAdmin))
}
# Register filters for this sub router.
register_filters(router, filters)

# Check if a command if followed by a value
pattern = r"^/\w+\ +\w+$"


@router.message(Command(commands.SuperAdmin.ADD_ADMIN), F.text.regexp(pattern))
async def add_admin(message: Message, bot: Bot):
    print("SUPERADMIN", True, message.text)


@router.message(Command(commands.SuperAdmin.REMOVE_ADMIN), F.text.regexp(pattern))
async def remove_admin(message: Message, bot: Bot):
    print(True)
    print(message.text)


@router.message(Command(*list(commands.SuperAdmin)), ~F.text.regexp(pattern))
async def incomplete_command(message: Message):
    print("SUPERADMIN", False, message.text)