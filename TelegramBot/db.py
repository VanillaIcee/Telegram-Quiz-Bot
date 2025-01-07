import aiosqlite
from config import DB_NAME

# Функция для создания таблиц в базе данных
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу для хранения состояния квиза (индекс вопроса для каждого пользователя)
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS quiz_state ( 
                user_id INTEGER PRIMARY KEY, 
                question_index INTEGER 
            )
        ''')

        # Создаем таблицу для хранения результатов квиза (правильные и неправильные ответы пользователя)
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS quiz_results ( 
                user_id INTEGER, 
                question_index INTEGER, 
                is_correct INTEGER 
            )
        ''')

        await db.commit()  # Сохраняем изменения в базе данных

# Функция для обновления индекса текущего вопроса для пользователя
async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем или обновляем индекс вопроса для пользователя
        await db.execute(''' 
            INSERT OR REPLACE INTO quiz_state (user_id, question_index) 
            VALUES (?, ?)
        ''', (user_id, index))
        await db.commit()

# Функция для получения текущего индекса вопроса для пользователя
async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0  # Если запись найдена, возвращаем индекс, иначе 0

# Функция для сохранения результата ответа пользователя на вопрос
async def save_user_result(user_id, question_index, correct):
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем результат ответа пользователя (1 - правильный, 0 - неправильный)
        await db.execute(''' 
            INSERT INTO quiz_results (user_id, question_index, is_correct) 
            VALUES (?, ?, ?)
        ''', (user_id, question_index, 1 if correct else 0))
        await db.commit()

async def show_user_statistics(user_id, message):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(''' 
            SELECT COUNT(*), COALESCE(SUM(is_correct), 0) 
            FROM quiz_results 
            WHERE user_id = ? 
        ''', (user_id,)) as cursor:
            total_questions, correct_answers = await cursor.fetchone()

        if total_questions == 0:
            await message.answer("Вы еще не прошли ни одного вопроса викторины.")
        else:
            await message.answer(f"Вы ответили на {total_questions} вопросов, из которых {correct_answers} были правильными.")

# Функция для начала нового квиза, очищая старые результаты
async def start_new_quiz(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Удаляем старые результаты для данного пользователя, чтобы начать новый квиз
        await db.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
        await db.commit()
