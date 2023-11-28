from typing import List

from aiogram import Router

from .admission_channel import router as admission_channel_root
from .private_chat import router as private_chat_root

routers: List[Router] = [
    private_chat_root,
    admission_channel_root,
]