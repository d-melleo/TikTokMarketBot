from datetime import datetime, timedelta
import json
from typing import Any, Dict, List, Union

from aiogram.types import BotCommand, User
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.server_api import ServerApi

from config import DB_COLLECTION_NAME, DB_CONNECTION_STRING, DB_NAME


class DBConnect:
    # client = AsyncIOMotorClient(connection_string, server_api=ServerApi("1", strict=True))
    client = AsyncIOMotorClient(DB_CONNECTION_STRING)
    db: AsyncIOMotorDatabase = client[DB_NAME]
    collection: AsyncIOMotorCollection = db[DB_COLLECTION_NAME]


class UserData:
    def __init__(
        self,
        data: Dict[str, Any],
        current_utc_time: datetime = datetime.utcnow()
    ) -> None:
        DEFAULT_USER_ROLE = "user"
        
        # _id (with underscore) replaces Mongo's default _id key.
        self._id: int = data.get('id', data.get('_id'))
        self.first_name: str = data.get('first_name')
        self.last_name: str = data.get('last_name')
        self.username: str = data.get('username')
        self.language_code: str = data.get('language_code')
        self.is_banned: bool = data.get('is_banned', False)
        self.role: str = data.get('role', DEFAULT_USER_ROLE)
        self.registration_date: datetime = data.get(
            'registration_date', current_utc_time)
        self.last_activity: datetime = data.get(
            'last_activity', current_utc_time)
        self.hold_until: datetime = data.get(
            'hold_until', current_utc_time)

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @staticmethod
    async def update_database(
        db_user: Dict[str, Any],
        tg_user: User,
        values: List[str]
    ) -> Dict[str, Any]:
        """Update user in DB

        Sometimes, users update their data in Telegram (name, username, etc.).
        This functions keeps Database up-to-date with users.
        """

        update_values: Dict[str, str] = {}

        if db_user['_id'] == tg_user.id:
            for value in values:
                if db_user[value] != tg_user.__dict__[value]:
                    db_user[value] = tg_user.__dict__[value]
                    update_values[value] = db_user[value]

        if update_values:
            await DBConnect.collection.update_one(
                {'_id': db_user['_id']},
                {'$set': update_values}
            )

        return db_user

    async def update_last_activity(self, current_utc_time: datetime) -> None:
        """Update last activity timestamp in DB after a hadnler's execution."""

        self.last_activity = current_utc_time
        await DBConnect.collection.update_one(
            {'_id': self._id},
            {'$set': {'last_activity': current_utc_time}}
        )


async def get_my_user(
    tg_user: User,
    current_utc_time: datetime = datetime.utcnow()
) -> UserData:
    my_user = None
    db_user: Dict[str, Any] | None = await DBConnect.collection.find_one({'_id': tg_user.id})

    if not db_user:
        my_user = UserData(tg_user.__dict__, current_utc_time)
        # Write user data into DB.
        await DBConnect.collection.insert_one(my_user.__dict__)

    else:
        # Update user's details in DB if anything has changed.
        db_user: Dict[str, Any] = await UserData.update_database(
            db_user,
            tg_user,
            values=["first_name", "last_name", "username"]
        )
        
        my_user = UserData(db_user, current_utc_time)

    return my_user