"""Telegram Bot

:bot_name: 📱TIK-TOK MARKET💰
:bot_username: @TikTok_MarketBot
"""

import asyncio
import logging
import sys

from bot.polling import polling_run
from bot.webhook import webhook_run
from aiogram.utils.formatting import Text, Bold, TextMention, as_list, as_line


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(polling_run())
