import aiosqlite
from aiogram import types
from config import DB_NAME


async def create_table(dataquiz):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER, question_index INTEGER, is_correct INTEGER)''')
        await db.commit()


async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def save_user_result(user_id, question_index, correct):
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу результатов
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER, question_index INTEGER, is_correct INTEGER)''')
        # Вставляем результат
        await db.execute('INSERT INTO quiz_results (user_id, question_index, is_correct) VALUES (?, ?, ?)', (user_id, question_index, 1 if correct else 0))
        await db.commit()
        
async def show_user_statistics(user_id, message):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*), SUM(is_correct) FROM quiz_results WHERE user_id = ?', (user_id,)) as cursor:
            total_questions, correct_answers = await cursor.fetchone()
    await message.answer(f"Вы ответили на {total_questions} вопросов, из которых {correct_answers} были правильными.")

async def start_new_quiz(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Удаляем старые результаты для данного пользователя
        await db.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
        await db.commit()
