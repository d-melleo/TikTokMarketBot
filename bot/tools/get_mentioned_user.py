from aiogram.enums import MessageEntityType
from aiogram.types import Message, User


def get_mentioned_user(message: Message) -> User:
    for entity in message.caption_entities:
        if entity.type == MessageEntityType.TEXT_MENTION:
            return entity.user