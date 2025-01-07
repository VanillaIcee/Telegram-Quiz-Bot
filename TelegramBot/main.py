import asyncio
import logging
from aiogram import Bot
from TelegramBot.db import create_table
from TelegramBot.config import API_TOKEN
import aiosqlite
from TelegramBot.handlers import dp
from TelegramBot.config import DB_NAME

# Создаем объект бота с использованием токена API
bot = Bot(token=API_TOKEN)

# Присваиваем объект бота диспетчеру
dp.bot = bot

# Основная асинхронная функция
async def main():
    # Открываем асинхронное соединение с базой данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу в базе данных, если она еще не существует
        await create_table()
    # Запускаем процесс опроса (polling) для обработки входящих сообщений
    await dp.start_polling(bot)

# Проверяем, является ли данный файл основным модулем
if __name__ == "__main__":
    # Настраиваем логирование на уровень INFO
    logging.basicConfig(level=logging.INFO)
    try:
        # Запускаем основную асинхронную функцию
        asyncio.run(main())
    except KeyboardInterrupt:
        # Обрабатываем прерывание программы (например, при нажатии Ctrl+C)
        print('Бот выключен')
