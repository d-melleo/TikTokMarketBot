import re

from aiogram import Bot, F, Router
from aiogram.filters import Command, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ....enums import commands, PrivateChatRoles
from ....messages.text import private_chat_admin as T
from ...states import AdminCommand
from ....tools.router_setup import register_filters
from db.userdata import UserData

# Sub router of the parent Router(name="private_chat_root")
router = Router(name="private_chat_admin")

filters = {
    MagicData(F.my_user.role.in_({
        PrivateChatRoles.ADMIN,
        PrivateChatRoles.SUPERADMIN,
        PrivateChatRoles.CREATOR
    }))
}
# Register filters for this sub router.
register_filters(router, filters)

# Check if a command if followed by a value
pattern = r"^/\w+\ +\w+$"


@router.message(Command(commands.Admin.BAN), F.text.regexp(pattern))
async def ban(message: Message, bot: Bot, **kwargs):
    username = kwargs.get("username")
    if not username:
        username: str = message.text.split()[1]
    if username != message.from_user.username:
        result: bool = await UserData.ban(username)
    else:
        result = None

    await bot.send_message(
        chat_id=message.chat.id,
        text=T.ban(username, result)
    )


@router.message(Command(commands.Admin.UNBAN), F.text.regexp(pattern))
async def unban(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(commands.Admin.HOLD), F.text.regexp(pattern))
async def hold(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(commands.Admin.RELEASE), F.text.regexp(pattern))
async def release(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(commands.Admin.GET_USER), F.text.regexp(pattern))
async def get_user(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(commands.Admin.BAN_LIST), F.text.regexp(pattern))
async def ban_list(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(commands.Admin.HOLD_LIST), F.text.regexp(pattern))
async def hold_list(message: Message, bot: Bot, username: str = None, *args):
    ...


@router.message(Command(*list(commands.Admin)), ~F.text.regexp(pattern))
async def incomplete_command(message: Message, bot: Bot, state: FSMContext, *args):
    await state.set_state(AdminCommand.incomplete_command)
    await state.update_data(command=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=T.incomplete_command(message.text)
    )


@router.message(AdminCommand.incomplete_command)
async def complete_command(message: Message, bot: Bot, state: FSMContext, my_user: UserData):
    data = await state.get_data()
    await state.clear()

    command = data.get("command")
    if command:
        command = re.sub(r"/", "", command)
        func = globals().get(command)
        await func(
            message=message,
            bot=bot,
            username=message.text
        )