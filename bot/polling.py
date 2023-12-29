from aiogram import Bot, Dispatcher

from . import dispatcher
from config.environment_vars import BOT_TOKEN


async def polling_run() -> None:
    """Run the polling process for handling incoming updates.

    This function initializes and sets up the aiogram dispatcher, creates an instance
    of the Bot using the specified BOT_TOKEN, and starts the polling process to receive
    updates from the Telegram Bot API. Any existing webhook is removed before polling
    begins to ensure a seamless transition.

    Note:
        Make sure to call this function within an asynchronous event loop.

    Example:
        To start the polling process, use this function as follows:

        >>> await polling_run()
    """
    # Initialize and set up the dispatcher
    dp: Dispatcher = dispatcher.initialize()

    # Create an instance of the Bot
    bot = Bot(BOT_TOKEN)

    # Remove any existing webhook and start the polling process
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)