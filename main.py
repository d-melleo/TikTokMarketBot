import asyncio
import logging
import sys

from bot.webhook import webhook_run
from bot.polling import polling_run


"@TikTok_MarketBot"
"📱TIK-TOK MARKET💰"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # webhook_run() # WEBHOOK
    asyncio.run(polling_run()) # POLLING