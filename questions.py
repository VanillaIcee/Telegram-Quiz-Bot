from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from db import update_quiz_index, get_quiz_index, start_new_quiz


# Данные для викторины, содержащие вопросы, варианты ответов и индекс правильного ответа 'correct_option'
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
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

# Функция для генерации клавиатуры с вариантами ответов
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder() # Создаем объект для построения клавиатуры
 
    # Добавляем кнопки для каждого варианта ответа
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1) # Настраиваем клавиатуру (например, количество кнопок в строке)
    return builder.as_markup() # Возвращаем клавиатуру в виде разметки

# Асинхронная функция для получения текущего вопроса и отправки его пользователю
async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)  # Получаем индекс текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']  # Индекс правильного ответа
    opts = quiz_data[current_question_index]['options']  # Варианты ответов
    kb = generate_options_keyboard(opts, opts[correct_index])  # Генерируем клавиатуру
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)  # Отправляем вопрос

# Асинхронная функция для начала новой викторины
async def new_quiz(message):
    user_id = message.from_user.id  # Получаем ID пользователя
    current_question_index = 0  # Устанавливаем индекс текущего вопроса на 0
    await update_quiz_index(user_id, current_question_index)  # Обновляем индекс вопроса в базе данных
    await start_new_quiz(user_id)  # Запускаем новую викторину
    await get_question(message, user_id)  # Отправляем первый вопрос