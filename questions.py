from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from db import update_quiz_index, get_quiz_index, start_new_quiz

# Данные для викторины
quiz_data = [
    # Список вопросов. Каждый вопрос содержит текст, варианты ответов и индекс правильного варианта.
    {
        'question': 'Что такое Python?',  # Текст вопроса
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],  # Варианты ответов
        'correct_option': 0  # Индекс правильного ответа в списке вариантов
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Что такое asyncio?',
        'options': ['Библиотека для многопоточности', 'Библиотека для дополненной реальности', 'Библиотека для асинхронного программирования', 'Библиотека для работы с сетью'],
        'correct_option': 2
    },
    {
        'question': 'Какой метод используется для добавления элемента в конец списка?',
        'options': ['append()', 'add()', 'insert()', 'extend()'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для доступа к элементам списка?',
        'options': ['()', '[]', '{}', '||'],
        'correct_option': 1
    },
    {
        'question': 'Что такое List Comprehension в Python?',
        'options': ['Способ создания списков', 'Тип данных', 'Набор функций', 'Модули в Python'],
        'correct_option': 0
    },
    {
        'question': 'Какой ключевое слово используется для определения функции?',
        'options': ['def', 'function', 'func', 'define'],
        'correct_option': 0
    },
    {
        'question': 'Как получить длину списка?',
        'options': ['len()', 'length()', 'size()', 'count()'],
        'correct_option': 0
    },
    {
        'question': 'Что такое декоратор в Python?',
        'options': ['Функция, изменяющая другую функцию', 'Класс', 'Модуль', 'Комплексное число'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод используется для чтения файла?',
        'options': ['open()', 'read()', 'load()', 'fetch()'],
        'correct_option': 1
    },
]

def generate_options_keyboard(answer_options, right_answer):
    """Создает инлайн-клавиатуру для вопроса."""
    builder = InlineKeyboardBuilder()  # Создаем объект для построения клавиатуры
    for option in answer_options:
        # Добавляем кнопку для каждого варианта ответа
        builder.add(types.InlineKeyboardButton(
            text=option,  # Текст кнопки
            callback_data="right_answer" if option == right_answer else "wrong_answer"  # Callback, указывающий правильный или неправильный ответ
        ))
    builder.adjust(1)  # Устанавливаем, чтобы кнопки располагались в одну колонку
    return builder.as_markup()  # Возвращаем готовую клавиатуру

async def get_question(message, user_id):
    """Отправляет текущий вопрос пользователю."""
    current_question_index = await get_quiz_index(user_id)  # Получаем текущий индекс вопроса для пользователя
    if current_question_index >= len(quiz_data):
        # Если вопросы закончились, вызываем функцию завершения квиза
        await finish_quiz(message)
        return
    correct_index = quiz_data[current_question_index]['correct_option']  # Индекс правильного варианта ответа
    opts = quiz_data[current_question_index]['options']  # Список вариантов ответа
    kb = generate_options_keyboard(opts, opts[correct_index])  # Создаем клавиатуру с вариантами ответа
    # Отправляем текст вопроса и клавиатуру пользователю
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    """Начинает новый квиз для пользователя."""
    user_id = message.from_user.id  # Получаем ID пользователя
    current_question_index = 0  # Устанавливаем текущий индекс вопроса на начало
    await update_quiz_index(user_id, current_question_index)  # Обновляем индекс в базе данных
    await start_new_quiz(user_id)  # Сбрасываем результаты предыдущего квиза
    await get_question(message, user_id)  # Отправляем первый вопрос

async def finish_quiz(message):
    """Завершает квиз и уведомляет пользователя."""
    # Сообщаем пользователю, что квиз завершен
    await message.answer("Это был последний вопрос. Квиз завершен!")
