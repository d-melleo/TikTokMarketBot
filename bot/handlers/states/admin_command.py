from aiogram.fsm.state import State, StatesGroup


class AdminCommand(StatesGroup):
    incomplete_command = State()