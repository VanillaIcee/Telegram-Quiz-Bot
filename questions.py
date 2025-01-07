from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from db import update_quiz_index, get_quiz_index, start_new_quiz

# Данные для викторины
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
] # Список вопросов и вариантов ответов

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()  # Создаем объект для построения клавиатуры
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"
        ))
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    if current_question_index >= len(quiz_data):
        await finish_quiz(message)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await start_new_quiz(user_id)
    await get_question(message, user_id)

async def finish_quiz(message):
    await message.answer("Это был последний вопрос. Квиз завершен!")
