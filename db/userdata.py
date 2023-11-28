from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from aiogram.types import BotCommand, User

from bot.private.enums.my_roles import MyRoles
from db.connect import DBConnect


class UserData:
    def __init__(
        self,
        data: Dict[str, Any],
        current_utc_time: datetime
    ) -> None:
        DEFAULT_USER_ROLE = MyRoles.USER
        
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

        self.commands: List[BotCommand] = None

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
        """Update user information in the database.

        This function is designed to synchronize user data in the database with
        changes made by users on Telegram, such as updates to their name, username, etc.
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
        """Update the last activity timestamp in the database after a handler's execution."""
        self.last_activity = current_utc_time
        await DBConnect.collection.update_one(
            {'_id': self._id},
            {'$set': {'last_activity': current_utc_time}}
        )


async def get_my_user(
    tg_user: User,
    current_utc_time: datetime
) -> UserData:
    """Retrieve or create a UserData instance for the given Telegram user.

    Args:
        tg_user (User): The Telegram user.
        current_utc_time (datetime): The current UTC time.

    Returns:
        UserData: The UserData instance for the specified Telegram user.
    """
    my_user = None
    db_user = await DBConnect.collection.find_one({'_id': tg_user.id})

    if not db_user:
        my_user = UserData(tg_user.__dict__, current_utc_time)
        # Write user data into DB.
        await DBConnect.collection.insert_one(my_user.__dict__)

    else:
        # Update user's details in DB if anything has changed.
        db_user = await UserData.update_database(
            db_user,
            tg_user,
            values=["first_name", "last_name", "username"]
        )
        
        my_user = UserData(db_user, current_utc_time)

    return my_user