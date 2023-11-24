import json
from datetime import datetime, timedelta
from typing import List, Any, Dict, Union

from aiogram.types import BotCommand, User

from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from config import DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION_NAME


class DBConnect:
    # client = AsyncIOMotorClient(connection_string, server_api=ServerApi("1", strict=True))
    client = AsyncIOMotorClient(DB_CONNECTION_STRING)
    db: AsyncIOMotorDatabase = client[DB_NAME]
    collection: AsyncIOMotorCollection = db[DB_COLLECTION_NAME]


class UserData:
    def __init__(
        self,
        data: Union[User, Dict[str, Any]],
        current_utc_time: datetime = datetime.utcnow()
    ) -> None:

        if isinstance(data, dict):
            self._id: int = data['_id']
            self.username: str = data['username']
            self.name: str = data['name']
            self.role: str = data['role']
            self.is_banned: bool = data['is_banned']
            self.language: str = data['language']
            self.registration_date: datetime = data['registration_date']
            self.last_activity: datetime = data['last_activity']
            self.hold_until: datetime = data['hold_until']

        elif isinstance(data, User):
            self._id: int = data.id
            self.username: str = data.username
            self.name: str = ('{} {}').format(data.first_name, data.last_name)
            self.role: str = 'user'
            self.is_banned: bool = False
            self.language: str = data.language_code
            self.registration_date: datetime = current_utc_time
            self.last_activity: datetime = current_utc_time
            self.hold_until: datetime = current_utc_time

        self.commands: List[BotCommand] = None


    def __call__(self) -> Dict[str, Any]:
        user_data = {
            '_id': self._id,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'is_banned': self.is_banned,
            'language': self.language,
            'registration_date': self.registration_date,
            'last_activity': self.last_activity,
            'hold_until': self.hold_until
        }
        return user_data


    def __str__(self) -> str:
        # Get user's detaiils
        user_data: Dict[str, Any] = self()

        # Convert the datetime objects to ISO 8601 format strings
        user_data['registration_date'] = user_data['registration_date'].isoformat()
        user_data['last_activity'] = user_data['last_activity'].isoformat()
        user_data['hold_until'] = user_data['hold_until'].isoformat()

        return json.dumps(user_data, indent=4)


    @staticmethod
    async def read_user(_id: int) -> Union[Dict[str, Any], None]:
        return await DBConnect.collection.find_one({'_id': _id})


    @staticmethod
    async def write_user(event_from_user: User, current_utc_time: datetime):
        my_user = UserData(event_from_user, current_utc_time)
        await DBConnect.collection.insert_one(my_user())
        return my_user


    @staticmethod
    async def validate_name(db_user: Dict[str, Any], event_from_user: User) -> Dict[str, Any]:
        # Check if name has not changed
        name: str = f'{event_from_user.first_name} {event_from_user.last_name}'

        if name != db_user['name']:
            await DBConnect.collection.update_one({'_id': db_user['_id']}, {'$set': {'name': name}})
            db_user['name'] = name
        return db_user


    @staticmethod
    async def validate_username(db_user: Dict[str, Any], event_from_user: User) -> Dict[str, Any]:
        # Check if username has not changed
        username: str = event_from_user.username

        if username != db_user['username']:
            await DBConnect.collection.update_one({'_id': db_user['_id']}, {'$set': {'username': username}})
            db_user['username'] = username
        return db_user


    async def update_last_activity(self, current_utc_time: datetime) -> None:
        # Update last activity record in DB
        await DBConnect.collection.update_one(
            {'_id': self._id}, {'$set': {'last_activity': current_utc_time}}
        )


    @staticmethod
    async def hold(username: str, current_utc_time: datetime, for_hours: Union[int, str] = 12) -> None:
        current = datetime.utcnow() # Get the current UTC time
        hold_until = current + timedelta(hours=int(for_hours)) # Add hours to the current time

        # Update database
        await DBConnect.collection.update_one({'username': username}, {'$set': {'hold_until': hold_until}})


    @staticmethod
    async def release(username: str, current_utc_time: datetime) -> None:
        hold_until = datetime.utcnow() # Get the current UTC time

        # Update database
        await DBConnect.collection.update_one({'username': username}, {'$set': {'hold_until': hold_until}})