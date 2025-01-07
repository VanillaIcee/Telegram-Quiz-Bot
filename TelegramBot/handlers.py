from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from TelegramBot.db import get_quiz_index, update_quiz_index, save_user_result, show_user_statistics
from TelegramBot.questions import get_question, new_quiz, quiz_data
from aiogram import F


dp = Dispatcher()  # Инициализация диспетчера для обработки входящих сообщений и событий

async def handle_answer(callback: types.CallbackQuery, is_correct: bool):
    """Обработка ответа (правильного или неправильного)."""
    # Убираем клавиатуру после того, как пользователь дал ответ
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None  # Удаляем текущую клавиатуру
    )
    
    # Получаем текущий индекс вопроса для пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    if is_correct:
        # Сообщаем пользователю, что его ответ верный
        await callback.message.answer("Верно!")
        # Сохраняем результат как правильный в базу данных
        await save_user_result(callback.from_user.id, current_question_index, correct=True)
    else:
        # Сообщаем пользователю, что его ответ неверный, и выводим правильный ответ
        correct_option = quiz_data[current_question_index]['correct_option']  # Индекс правильного ответа
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
        # Сохраняем результат как неправильный в базу данных
        await save_user_result(callback.from_user.id, current_question_index, correct=False)

    # Увеличиваем индекс текущего вопроса, чтобы перейти к следующему
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    # Проверяем, есть ли следующий вопрос
    if current_question_index < len(quiz_data):
        # Если вопросы остались, отправляем следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Если вопросы закончились, завершаем викторину
        await finish_quiz(callback.message, callback.from_user.id)

from TelegramBot.db import show_user_statistics


@dp.callback_query(F.data == "right_answer")  # Обработка правильного ответа
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True)  # Передаем обработку в общую функцию

@dp.callback_query(F.data == "wrong_answer")  # Обработка неправильного ответа
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False)  # Передаем обработку в общую функцию

async def finish_quiz(message, user_id):
    """Функция для завершения квиза."""
    # Уведомляем пользователя, что викторина завершена
    await message.answer("Это был последний вопрос. Квиз завершен!")
    # Показываем статистику пользователя
    await show_user_statistics(user_id, message)

@dp.message(F.text == "Начать игру")  # Обработка нажатия кнопки "Начать игру"
@dp.message(Command("quiz"))  # Обработка команды /quiz
async def cmd_quiz(message: types.Message):
    # Уведомляем пользователя, что викторина начинается
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз, используя функцию из другого модуля
    await new_quiz(message)

@dp.message(Command("start"))  # Обработка команды /start
async def cmd_start(message: types.Message):
    # Создаем объект клавиатуры с кнопками
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))  # Кнопка "Начать игру"
    builder.add(types.KeyboardButton(text="Показать статистику"))  # Кнопка "Показать статистику"
    # Отправляем пользователю приветственное сообщение и клавиатуру
    await message.answer(
        "Добро пожаловать в квиз!\n\n"
        "Вы можете:\n"
        "- Нажать «Начать игру», чтобы пройти викторину.\n"
        "- Нажать «Показать статистику», чтобы увидеть свои результаты.\n\n"
        "Также доступны команды:\n"
        "- /quiz — начать новую игру\n"
        "- /stats — показать статистику.",
        reply_markup=builder.as_markup(resize_keyboard=True)  # Отображаем клавиатуру с кнопками
    )

@dp.message(F.text == "Показать статистику")  # Обработка нажатия кнопки "Показать статистику"
async def cmd_show_stats(message: types.Message):
    # Получаем ID пользователя
    user_id = message.from_user.id
    # Показываем пользователю статистику, вызвав соответствующую функцию
    await show_user_statistics(user_id, message)
