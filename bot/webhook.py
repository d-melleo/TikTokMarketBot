from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from . import dispatcher
from config.environment_vars import BOT_TOKEN, WEBHOOK_URI



async def register_webhook(bot: Bot, webhook_uri: str = WEBHOOK_URI) -> None:
    """Register a webhook with the Telegram Bot API.

    This function removes any existing webhook and sets a new one with the specified
    webhook_uri. The webhook can also be registered manually in a browser using the
    provided URL format.

    https://api.telegram.org/bot6355498787:AAHIXifH_NGLeGeJLAidFJ5aLIFjRgx_YTk/setWebhook?url={webhook_uri}
    

    Args:
        bot (Bot): The Bot instance to register the webhook with.
        webhook_uri (str): The URI to set as the new webhook. Defaults to WEBHOOK_URI.
    """

    await bot.delete_webhook(drop_pending_updates=True)  # Remove the current webhook if any.
    await bot.set_webhook(f'{webhook_uri}')  # Register a new webhook.


async def on_shutdown(bot: Bot) -> None:
    # Unregister the webhook on shutdown.
    await bot.delete_webhook(drop_pending_updates=True)


def webhook_run():
    # Initialize and set up the dispatcher.
    dp: Dispatcher = dispatcher.initialize()
    dp.startup.register(register_webhook)
    dp.shutdown.register(on_shutdown)

    # Create a Bot instance with specified settings for API calls.
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Create an aiohttp web application.
    app = web.Application()

    # Initialize a request handler instance for handling webhook requests.
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)

    # Register the webhook handler on the web application.
    webhook_requests_handler.register(app, path='')

    # Mount dispatcher startup and shutdown hooks to the aiohttp application.
    setup_application(app, dp, bot=bot)

    # Start the web server.
    web.run_app(app, host='127.0.0.1', port=3000)