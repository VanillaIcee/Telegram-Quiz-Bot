import aiosqlite
from config import DB_NAME

# Функция для создания таблиц в базе данных
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу для хранения состояния квиза
        # В этой таблице хранится индекс текущего вопроса для каждого пользователя
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS quiz_state ( 
                user_id INTEGER PRIMARY KEY,  # Уникальный идентификатор пользователя
                question_index INTEGER        # Индекс текущего вопроса
            )
        ''')

        # Создаем таблицу для хранения результатов квиза
        # Здесь хранятся ответы пользователя: правильные и неправильные
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS quiz_results ( 
                user_id INTEGER,            # Идентификатор пользователя
                question_index INTEGER,     # Индекс вопроса, на который был дан ответ
                is_correct INTEGER          # 1, если ответ правильный; 0, если неправильный
            )
        ''')

        await db.commit()  # Сохраняем изменения в базе данных

# Функция для обновления индекса текущего вопроса для пользователя
async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или обновляем существующую
        # Если запись с таким user_id уже существует, она заменяется
        await db.execute(''' 
            INSERT OR REPLACE INTO quiz_state (user_id, question_index) 
            VALUES (?, ?)  # Заменяем user_id и question_index значениями из параметров
        ''', (user_id, index))
        await db.commit()

# Функция для получения текущего индекса вопроса для пользователя
async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем запрос для получения индекса текущего вопроса из таблицы quiz_state
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()  # Получаем первую (и единственную) строку результата
            return result[0] if result else 0  # Если запись существует, возвращаем индекс; иначе 0

# Функция для сохранения результата ответа пользователя на вопрос
async def save_user_result(user_id, question_index, correct):
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем результат ответа пользователя
        # Используем 1, если ответ правильный, или 0, если неправильный
        await db.execute(''' 
            INSERT INTO quiz_results (user_id, question_index, is_correct) 
            VALUES (?, ?, ?)
        ''', (user_id, question_index, 1 if correct else 0))
        await db.commit()

# Функция для отображения статистики пользователя
async def show_user_statistics(user_id, message):
    async with aiosqlite.connect(DB_NAME) as db:
        # Запрашиваем общее количество вопросов и сумму правильных ответов
        async with db.execute(''' 
            SELECT COUNT(*), COALESCE(SUM(is_correct), 0) 
            FROM quiz_results 
            WHERE user_id = ? 
        ''', (user_id,)) as cursor:
            total_questions, correct_answers = await cursor.fetchone()

        # Если пользователь еще не ответил ни на один вопрос
        if total_questions == 0:
            await message.answer("Вы еще не прошли ни одного вопроса викторины.")
        else:
            # Отправляем пользователю статистику о его ответах
            await message.answer(f"Вы ответили на {total_questions} вопросов, из которых {correct_answers} были правильными.")

# Функция для начала нового квиза, очищая старые результаты
async def start_new_quiz(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Удаляем все результаты, связанные с указанным user_id
        # Это позволяет начать викторину с нуля
        await db.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
        await db.commit()
