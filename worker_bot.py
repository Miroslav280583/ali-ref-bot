import asyncio
import logging
import os
from aiogram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1001234567890  # <-- заміни на свій справжній channel_id

bot = Bot(token=TOKEN, parse_mode="HTML")

products = [
    {
        "title": "Розумний годинник 2024",
        "url": "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/https://www.aliexpress.com/item/1005002345678901.html",
        "image": "https://http.cat/200.jpg"
    },
    {
        "title": "Портативна колонка з Bluetooth",
        "url": "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/https://www.aliexpress.com/item/1005006543210987.html",
        "image": "https://http.cat/201.jpg"
    }
]

async def post_to_channel():
    while True:
        for product in products:
            caption = f"<b>{product['title']}</b>\n<a href='{product['url']}'>Перейти до товару</a>"
            try:
                await bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=product["image"],
                    caption=caption
                )
                print(f"✅ Надіслано: {product['title']}")
            except Exception as e:
                logging.error(f"❌ Помилка: {e}")
            await asyncio.sleep(3600)  # затримка 1 година між постами

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(post_to_channel())