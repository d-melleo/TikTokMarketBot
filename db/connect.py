from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.server_api import ServerApi

from config.environment_vars import DB_COLLECTION_NAME, DB_CONNECTION_STRING, DB_NAME


class DBConnect:
    """A class representing a MongoDB connection using AsyncIOMotorClient.

    Attributes:
        client (AsyncIOMotorClient): The MongoDB client connected to the specified database.
        db (AsyncIOMotorDatabase): The MongoDB database instance accessed through the client.
        collection (AsyncIOMotorCollection): The MongoDB collection within the specified database.

    Note:
        Ensure that the class is used within an asynchronous context, as it utilizes
        AsyncIOMotorClient for asynchronous MongoDB operations.
    """
    # client = AsyncIOMotorClient(connection_string, server_api=ServerApi("1", strict=True))
    client = AsyncIOMotorClient(DB_CONNECTION_STRING)
    db: AsyncIOMotorDatabase = client[DB_NAME]
    collection: AsyncIOMotorCollection = db[DB_COLLECTION_NAME]