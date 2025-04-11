
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002638030609

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

products = [
    {
        "title": "Супер крутий гаджет для дому",
        "url": "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/https://www.aliexpress.com/item/1005001234567890.html",
        "image": "https://ae01.alicdn.com/kf/S4c3e2ff5ef174da28b24c19a3d2d4b10n.jpg"
    },
    {
        "title": "Годинник майбутнього",
        "url": "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/https://www.aliexpress.com/item/1005002345678901.html",
        "image": "https://ae04.alicdn.com/kf/Hc13a7d8d4b1b4cbf8ecf30c95d8ed26a8.jpg"
    }
]

async def post_to_channel():
    while True:
        product = products[datetime.now().hour % len(products)]
        caption = f"<b>{product['title']}</b>\n<a href='{product['url']}'>Перейти до товару</a>"
        try:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=product["image"],
                caption=caption
            )
            print(f"✅ Пост надіслано до {CHANNEL_ID}")
        except Exception as e:
            logging.error(f"❌ Помилка: {e}")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(post_to_channel())
