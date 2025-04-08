import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")

REF_PREFIX = "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def handle_message(message: Message):
    if "aliexpress.com/item/" in message.text:
        parts = message.text.split("https://www.aliexpress.com/item/")
        links = [part.strip().split()[0] for part in parts[1:]]
        reply_text = ""
        for link in links:
            full_link = "https://www.aliexpress.com/item/" + link
            ref_link = REF_PREFIX + full_link
            reply_text += f"Ось твій реферальний лінк:
{ref_link}

"
        await message.reply(reply_text.strip())
    else:
        await message.reply("Надішли мені посилання з AliExpress, і я зроблю його реферальним.")

async def on_startup(app):
    await bot.set_webhook(f"{APP_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, dp._as_webhook_handler(secret_token=WEBHOOK_SECRET))
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
