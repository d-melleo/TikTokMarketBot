from os import environ
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


load_dotenv()  # load variables from virtual environment

# Path to the root directory
WORKDIR = Path(__file__).parent.parent

# Bot constants
BOT_TOKEN: str = environ.get('BOT_TOKEN')
CHANNELS: Dict[str, int] = {
    'admissions': int(environ.get('ADMISSIONS_CHANNEL_ID'))
}

# Webhook
WEBHOOK_PATH: str = environ.get('WEBHOOK_PATH')
WEB_SERVER_HOST: str = environ.get('WEB_SERVER_HOST')
WEB_SERVER_PORT: str = environ.get('WEB_SERVER_PORT')

# Database constants
DB_NAME: str = environ.get('DB_NAME')
DB_COLLECTION_NAME: str = environ.get('DB_COLLECTION_NAME')
DB_CONNECTION_STRING: str = environ.get('DB_CONNECTION_STRING')

print(DB_NAME)
print(DB_COLLECTION_NAME)
print(DB_CONNECTION_STRING)