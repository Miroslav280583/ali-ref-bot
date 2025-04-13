import os
import asyncio
import logging
import random
from aiogram import Bot
import aiohttp

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002638030609  # <-- заміни на свій справжній channel_id
REF_PREFIX = "https://rzekl.com/g/1e8d114494fa41a0c5ab16525dc3e8/?ulp="

bot = Bot(token=TOKEN, parse_mode="HTML")

# Приклад: запит на топ товари (можна замінити джерело)
async def fetch_random_product():
    url = "https://www.aliexpress.com/category/100003109/women-clothing.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()

    # Простий парсинг (шукаємо посилання на товари)
    links = []
    for line in html.splitlines():
        if 'href="' in line and 'item/' in line:
            start = line.find('href="') + 6
            end = line.find('"', start)
            link = line[start:end]
            if "http" not in link:
                link = "https:" + link
            if link not in links and "aliexpress.com/item" in link:
                links.append(link)

    if not links:
        raise ValueError("Не знайдено товарів")

    product_url = random.choice(links)
    image = "https://http.cat/200.jpg"  # тимчасово, бо реальні фото важко парсити
    return {
        "title": "Топ товар з AliExpress",
        "url": REF_PREFIX + product_url,
        "image": image
    }

async def post_to_channel():
    while True:
        try:
            product = await fetch_random_product()
            caption = f"<b>{product['title']}</b>\n<a href='{product['url']}'>Перейти до товару</a>"
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=product["image"],
                caption=caption
            )
            print("✅ Товар опубліковано")
        except Exception as e:
            logging.error(f"❌ Помилка при надсиланні: {e}")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(post_to_channel())
