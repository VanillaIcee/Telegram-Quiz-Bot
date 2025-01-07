from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from db import get_quiz_index, update_quiz_index, save_user_result, show_user_statistics
from questions import get_question, new_quiz, quiz_data

dp = Dispatcher()  # Инициализация диспетчера для обработки входящих сообщений и событий

@dp.message(Command("start"))  # Обработка команды /start
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()  # Создание кнопок для клавиатуры
    builder.add(types.KeyboardButton(text="Начать игру"))  # Добавление кнопки "Начать игру"
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))  # Отправка приветственного сообщения и отображение клавиатуры

@dp.callback_query(F.data == "right_answer")  # Обработка нажатия кнопки с правильным ответом
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None  # Убираем клавиатуру после ответа
    )
    
    await callback.message.answer("Верно!")  # Сообщаем пользователю о правильном ответе
    current_question_index = await get_quiz_index(callback.from_user.id)  # Получение текущего индекса вопроса
    # Сохранение результата правильного ответа
    await save_user_result(callback.from_user.id, current_question_index, correct=True)

    current_question_index += 1  # Переход к следующему вопросу
    await update_quiz_index(callback.from_user.id, current_question_index)  # Обновление индекса в базе данных

    if current_question_index < len(quiz_data):  # Проверка, остались ли еще вопросы
        await get_question(callback.message, callback.from_user.id)  # Получение следующего вопроса
    else:
        await finish_quiz(callback.message, callback.from_user.id)  # Завершение квиза, если вопросы закончились

@dp.callback_query(F.data == "wrong_answer")  # Обработка нажатия кнопки с неправильным ответом
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None  # Убираем клавиатуру после ответа
    )

    current_question_index = await get_quiz_index(callback.from_user.id)  # Получение текущего индекса вопроса
    correct_option = quiz_data[current_question_index]['correct_option']  # Получение правильного варианта ответа

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")  # Информируем пользователя о неправильном ответе
    # Сохранение результата неправильного ответа
    await save_user_result(callback.from_user.id, current_question_index, correct=False)

    current_question_index += 1  # Переход к следующему вопросу
    await update_quiz_index(callback.from_user.id, current_question_index)  # Обновление индекса в базе данных

    if current_question_index < len(quiz_data):  # Проверка, остались ли еще вопросы
        await get_question(callback.message, callback.from_user.id)  # Получение следующего вопроса
    else:
        await finish_quiz(callback.message, callback.from_user.id)  # Завершение квиза, если вопросы закончились
        
# Функция для завершения квиза
async def finish_quiz(message, user_id):
    await message.answer("Это был последний вопрос. Квиз завершен!")  # Уведомление о завершении квиза
    # Вывод статистики по пользователю
    await show_user_statistics(user_id, message)

@dp.message(F.text == "Начать игру")  # Обработка нажатия кнопки "Начать игру"
@dp.message(Command("quiz"))  # Обработка команды /quiz
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")  # Уведомление о начале квиза
    await new_quiz(message)  # Запуск новой игры