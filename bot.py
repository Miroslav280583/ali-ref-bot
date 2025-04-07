
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def handle_message(message: Message):
    if "http" in message.text:
        await message.reply("Твій реферальний лінк: [тут буде логіка]")
    else:
        await message.reply("Надішли мені посилання з AliExpress, і я зроблю його реферальним.")

async def on_startup(app):
    await bot.set_webhook(f"{APP_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=WEBHOOK_SECRET
).register(app, path=WEBHOOK_PATH)

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    setup_application(app, dp)
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
