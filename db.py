import aiosqlite 
from config import DB_NAME 


async def create_table(dataquiz):
    # Функция для создания таблиц в базе данных, если они не существуют
    async with aiosqlite.connect(DB_NAME) as db:  # Создаем асинхронное подключение к базе данных
        # Создаем таблицу для хранения состояния квиза (индекс вопроса для каждого пользователя)
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Создаем таблицу для хранения результатов квиза (правильные и неправильные ответы пользователя)
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER, question_index INTEGER, is_correct INTEGER)''')
        await db.commit()  # Сохраняем изменения в базе данных


async def update_quiz_index(user_id, index):
    # Функция для обновления индекса текущего вопроса для заданного пользователя
    async with aiosqlite.connect(DB_NAME) as db:  # Создаем соединение с базой данных
        # Вставляем новую запись или заменяем существующую для пользователя с данным user_id
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()  # Сохраняем изменения


async def get_quiz_index(user_id):
    # Функция для получения текущего индекса вопроса для заданного пользователя
    async with aiosqlite.connect(DB_NAME) as db:  # Подключаемся к базе данных
        # Запрашиваем текущий индекс вопроса для пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Извлекаем результат запроса
            results = await cursor.fetchone()
            if results is not None:  # Если запись найдена
                return results[0]  # Возвращаем текущий индекс вопроса
            else:
                return 0  # Если записи нет, возвращаем 0 (начальный индекс)


async def save_user_result(user_id, question_index, correct):
    # Функция для сохранения результата ответа пользователя на вопрос
    async with aiosqlite.connect(DB_NAME) as db:  # Создаем соединение с базой данных
        # Создаем таблицу для результатов, если она не существует
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER, question_index INTEGER, is_correct INTEGER)''')
        # Вставляем результат ответа пользователя (1 - правильный, 0 - неправильный)
        await db.execute('INSERT INTO quiz_results (user_id, question_index, is_correct) VALUES (?, ?, ?)', (user_id, question_index, 1 if correct else 0))
        await db.commit()  # Сохраняем изменения


async def show_user_statistics(user_id, message):
    # Функция для показа статистики пользователя по ответам на вопросы
    async with aiosqlite.connect(DB_NAME) as db:  # Подключаемся к базе данных
        # Запрашиваем общее количество вопросов и количество правильных ответов для данного пользователя
        async with db.execute('SELECT COUNT(*), SUM(is_correct) FROM quiz_results WHERE user_id = ?', (user_id,)) as cursor:
            total_questions, correct_answers = await cursor.fetchone()  # Извлекаем результаты
    # Отправляем сообщение с информацией о статистике пользовательских ответов
    await message.answer(f"Вы ответили на {total_questions} вопросов, из которых {correct_answers} были правильными.")


async def start_new_quiz(user_id):
    # Функция для начала нового квиза, очищая старые результаты
    async with aiosqlite.connect(DB_NAME) as db:  # Создаем соединение с базой данных
        # Удаляем старые результаты для данного пользователя, чтобы начать новый квиз
        await db.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
        await db.commit()  # Сохраняем изменения