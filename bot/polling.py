from aiogram import Bot, Dispatcher

from . import dispatcher
from config import BOT_TOKEN


async def polling_run() -> None:
    # Set up the dispatcher
    dp: Dispatcher = await dispatcher.initialize()

    # Create Bot instance
    bot = Bot(BOT_TOKEN)

    # Remove webhook, start polling.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)