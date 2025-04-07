import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text)
async def handle_message(message: Message):
    if "http" in message.text:
        await message.reply("Твій реферальний лінк: [тут буде логіка]")
    else:
        await message.reply("Надішли мені посилання з AliExpress, і я зроблю його реферальним.")

async def on_startup(app: web.Application):
    await bot.set_webhook(
        url=f"{APP_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET
    )

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

async def handle_webhook(request: web.Request):
    return await dp._router.resolve(request)

app = web.Application()
app.add_routes([web.post(WEBHOOK_PATH, handle_webhook)])
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    import asyncio

    async def main():
        await on_startup(app)
        try:
            web.run_app(app, port=int(os.getenv("PORT", 10000)))
        finally:
            await on_shutdown(app)
