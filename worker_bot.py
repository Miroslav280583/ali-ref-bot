
import os
import asyncio
import aiohttp
from aiogram import Bot
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@AliTopDeals"
REF_PREFIX = "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/?ulp="

bot = Bot(token=BOT_TOKEN)

async def fetch_random_product():
    # Спрощено: фіксоване посилання, щоб перевірити логіку
    return {
        "title": "🔥 Топ-продукт з AliExpress",
        "url": "https://www.aliexpress.com/item/1005001234567890.html",
        "price": "19.99",
        "image": "https://ae01.alicdn.com/kf/HTB1.product_image.jpg"
    }

async def send_post():
    product = await fetch_random_product()
    ref_link = REF_PREFIX + product["url"]

    caption = f"<b>{product['title']}</b>
Ціна: ${product['price']}
"
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купити на AliExpress", url=ref_link)]
    ])

    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=product["image"],
            caption=caption,
            reply_markup=button,
            parse_mode="HTML"
        )
        print("✅ Пост відправлено")
    except Exception as e:
        print("❌ Помилка при відправленні посту:", e)

async def main_loop():
    while True:
        await send_post()
        await asyncio.sleep(3600)  # 1 година

if __name__ == "__main__":
    asyncio.run(main_loop())
