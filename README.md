#  Telegram Quiz Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Описание

**Telegram Quiz Bot** — Этот проект представляет собой Telegram-бота, созданного с использованием библиотеки aiogram, который предназначен для проведения квизов. Бот обеспечивает взаимодействие с пользователем, предоставляя ему возможность отвечать на вопросы и получать обратную связь о своих ответах. Основная цель бота — помочь пользователю проверить свои знания в различных областях. 

[Как выглядит мой бот в Telegram](https://t.me/NewSampleQuizBot)

## Функциональные возможности

- **Создание викторин**: Пользователи могут создавать викторины с настраиваемыми вопросами и ответами.
- **Прохождение викторин**: Участники могут проходить викторины, получая баллы за правильные ответы.
- **Анализ результатов**: Бот предоставляет возможности просматривать статистику и результаты прошедших викторин.
- **Поддержка нескольких языков**: Бот поддерживает многоязычные интерфейсы и вопросы.
- **Хранение данных**: Все результаты и статистика хранятся в базе данных, обеспечивая доступ и анализ данных для администраторов.

### Установка и настройка

Следуйте этим простым шагам, чтобы установить и запустить бота для квизов:

#### 1. Клонируйте репозиторий

Сначала необходимо клонировать репозиторий на вашу локальную машину. Откройте терминал и выполните команду:

```bash
git clone https://github.com/VanillaIcee/Telegram-Quiz-Bot
cd Telegram-Quiz-Bot
```

#### 2. Установите зависимости

Убедитесь, что у вас установлен Python 3.7 и выше. Затем установите необходимые библиотеки с помощью `pip`. Выполните команду:

```bash
pip install -r requirements.txt
```

#### 3. Настройте токен бота

Получите токен вашего бота от [BotFather](https://t.me/botfather) в Telegram. Создайте файл `config.py` (если его еще нет) и добавьте в него ваш токен, как показано ниже:

```python
API_TOKEN = 'Ваш_токен_бота_здесь'
DB_NAME = 'dataquiz.db'
```

#### 4. Запустите бота

Теперь все готово! Чтобы запустить бота, выполните команду:

```bash
python main.py
```

После выполнения этих шагов ваш бот будет запущен и готов к использованию!

#### 5. (Опционально) Создание базы данных

Бот автоматически создаст нужные таблицы в базе данных при первом запуске. Но если вы хотите сделать это вручную, вы можете использовать функции из `db.py` для создания необходимых таблиц.

### Дополнительные настройки

Если вы хотите настроить Quiz, отредактируйте файлы в проекте, такие как `questions.py`, чтобы добавить или изменить вопросы.

### Примечания

- Убедитесь, что у вас установлен Python 3.7 или выше.
- Бот работает на библиотеке `aiogram 3`, поэтому убедитесь, что у вас есть доступ к интернету для установки необходимых зависимостей.

## Технологии

- Python
- SQLite для хранения данных
- aiogram

## Вклад

Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория, внесите необходимые изменения и откройте Pull Request.

## Лицензия

Этот проект лицензирован на условиях лицензии MIT. 

---
