from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db import get_quiz_index, update_quiz_index, save_user_result, show_user_statistics
from questions import get_question, new_quiz, quiz_data
from aiogram import F


dp = Dispatcher()  # Инициализация диспетчера для обработки входящих сообщений и событий

async def handle_answer(callback: types.CallbackQuery, is_correct: bool):
    """Обработка ответа (правильного или неправильного)."""
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None  # Убираем клавиатуру после ответа
    )
    
    current_question_index = await get_quiz_index(callback.from_user.id)  # Получаем текущий индекс вопроса
    if is_correct:
        await callback.message.answer("Верно!")  # Сообщаем о правильном ответе
        await save_user_result(callback.from_user.id, current_question_index, correct=True)
    else:
        correct_option = quiz_data[current_question_index]['correct_option']  # Правильный вариант ответа
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")  # Сообщаем о неправильном ответе
        await save_user_result(callback.from_user.id, current_question_index, correct=False)

    # Переход к следующему вопросу
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    # Проверка, есть ли следующие вопросы
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)  # Переход к следующему вопросу
    else:
        await finish_quiz(callback.message, callback.from_user.id)  # Завершение квиза

from db import show_user_statistics


@dp.callback_query(F.data == "right_answer")  # Обработка правильного ответа
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True)

@dp.callback_query(F.data == "wrong_answer")  # Обработка неправильного ответа
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False)

async def finish_quiz(message, user_id):
    """Функция для завершения квиза."""
    await message.answer("Это был последний вопрос. Квиз завершен!")  # Уведомление о завершении квиза
    # Вывод статистики по пользователю
    await show_user_statistics(user_id, message)

@dp.message(F.text == "Начать игру")  # Обработка нажатия кнопки "Начать игру"
@dp.message(Command("quiz"))  # Обработка команды /quiz
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")  # Уведомление о начале квиза
    await new_quiz(message)  # Запуск новой игры

@dp.message(Command("start"))  # Обработка команды /start
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()  # Создание кнопок для клавиатуры
    builder.add(types.KeyboardButton(text="Начать игру"))  # Добавление кнопки "Начать игру"
    builder.add(types.KeyboardButton(text="Показать статистику"))  # Добавление кнопки "Показать статистику"
    await message.answer(
        "Добро пожаловать в квиз!\n\n"
        "Вы можете:\n"
        "- Нажать «Начать игру», чтобы пройти викторину.\n"
        "- Нажать «Показать статистику», чтобы увидеть свои результаты.\n\n"
        "Также доступны команды:\n"
        "- /quiz — начать новую игру\n"
        "- /stats — показать статистику.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message(F.text == "Показать статистику")  # Обработка нажатия кнопки "Показать статистику"
async def cmd_show_stats(message: types.Message):
    user_id = message.from_user.id  # Получаем ID пользователя
    await show_user_statistics(user_id, message)  # Вызываем функцию для отображения статистики
