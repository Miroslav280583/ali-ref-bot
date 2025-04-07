
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", 10000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text)
async def handle_message(message: Message):
    if "http" in message.text:
        await message.reply("Твій реферальний лінк: [тут буде логіка]")
    else:
        await message.reply("Надішли мені посилання з AliExpress, і я зроблю його реферальним.")

async def on_startup(app: web.Application):
    await bot.set_webhook(f"{APP_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, dp.webhook_handler(webhook_secret=WEBHOOK_SECRET))
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, port=PORT)
