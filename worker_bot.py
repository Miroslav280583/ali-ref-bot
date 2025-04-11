import logging
import os
import asyncio
from aiogram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002638030609  # заміни на свій справжній channel_id

bot = Bot(token=TOKEN, parse_mode="HTML")

product = {
    "title": "Годинник майбутнього",
    "url": "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/https://www.aliexpress.com/item/1005002345678901.html",
    "image": "https://ae04.alicdn.com/kf/S9a282bd8f0f14f3da623b2dc96e4e401e.jpg"
}

async def send_test_post():
    caption = f"<b>{product['title']}</b>\n<a href='{product['url']}'>Перейти до товару</a>"
    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=product["image"],
            caption=caption
        )
        print("✅ Тестовий пост надіслано")
    except Exception as e:
        logging.error(f"❌ Помилка при надсиланні: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(send_test_post())
