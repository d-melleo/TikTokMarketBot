from os import getenv
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


load_dotenv() # load .env

WORKDIR = Path(__file__).parent # Root directory path

BOT_TOKEN: str = getenv('BOT_TOKEN')
WEBHOOK_URI: str = getenv('WEBHOOK_URI')

CHANNELS: Dict[str, int] = {
    'admissions': int(getenv('ADMISSIONS_CHANNEL_ID'))
}

DB_CONNECTION_STRING: str = getenv('DB_CONNECTION_STRING')
DB_NAME: str = getenv('DB_NAME')
DB_COLLECTION_NAME: str = getenv('DB_COLLECTION_NAME')