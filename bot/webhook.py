from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from . import dispatcher
from config import BOT_TOKEN, WEBHOOK_URI


async def register_webhook(bot: Bot) -> None:
    # https://api.telegram.org/bot6355498787:AAHIXifH_NGLeGeJLAidFJ5aLIFjRgx_YTk/setWebhook?url=https://2dbc-178-158-205-163.ngrok-free.app

    await bot.delete_webhook(drop_pending_updates=True) # Remove prior webhook
    await bot.set_webhook(f'{WEBHOOK_URI}') # Register a webhook


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True) # Remove a webhook on shutdown


def webhook_run():
    # Set up the dispatcher
    dp: Dispatcher = dispatcher.initialize()

    # Register startup hook to initialize webhook
    dp.startup.register(register_webhook)
    dp.shutdown.register(on_shutdown)

    # Create bot instance, which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)

    # Register webhook handler on application
    # webhook_requests_handler.register(app, path=f'/{WEBHOOK}')
    webhook_requests_handler.register(app, path='')

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # Start webserver
    web.run_app(app, host='127.0.0.1', port=3000)