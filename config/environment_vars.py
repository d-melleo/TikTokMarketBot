from os import getenv
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


load_dotenv()  # load variables from virtual environment

# Path to the root directory
WORKDIR = Path(__file__).parent.parent

# Bot constants
BOT_TOKEN: str = getenv('BOT_TOKEN')

CHANNELS: Dict[str, int] = {
    'admissions': int(getenv('ADMISSIONS_CHANNEL_ID'))
}

# Webhook
WEBHOOK_PATH: str = getenv('WEBHOOK_PATH')
WEB_SERVER_HOST: str = getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT: str = getenv('WEB_SERVER_PORT')

# Database constants
DB_NAME: str = getenv('DB_NAME')
DB_COLLECTION_NAME: str = getenv('DB_COLLECTION_NAME')
DB_CONNECTION_STRING: str = getenv('DB_CONNECTION_STRING')