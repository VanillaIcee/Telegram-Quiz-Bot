import asyncio
import logging
from aiogram import Bot 
from db import create_table
from config import API_TOKEN
import aiosqlite
from handlers import dp
from config import DB_NAME

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Объект бота и диспетчер
bot = Bot(token = API_TOKEN)

dp.bot = bot

async def main():
    async with aiosqlite.connect(DB_NAME) as db:
        await create_table(db)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
