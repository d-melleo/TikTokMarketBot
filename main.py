import asyncio
import logging
import sys

from bot.polling import polling_run
from bot.webhook import webhook_run


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(polling_run())
    # webhook_run()
