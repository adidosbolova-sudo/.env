
import logging
import random
import json
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Токен Telegram-бота
TOKEN = "9200101111:AAFmHQa9BPFsblJmBP0JdiksVJP13hofK-Y"

# Файл для хранения профилей
FILE_NAME = "user.json"

# Словарь для хранения данных пользователей
user_data = {}

# Состояния диалога
NAME, COLOR = range(2)


# Загрузка данных из JSON-файла
def load_users():
    global user_data

    # Проверяем, существует ли файл
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            user_data = json.load(file)
    else:
        user_data = {}


# Сохранение данных в JSON-файл
def save_users():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            user_data,
            file,
            ensure_ascii=False,
            indent=4
        )


# Список заданий
tasks = [
    "📚 Прочитай 10 страниц интересной книги.",
    "🚶 Прогуляйся на свежем воздухе 30 минут.",
    "💧 Выпей достаточное количество воды сегодня.",
    "🧹 Наведи порядок на рабочем столе.",
    "🧠 Выучи 5 новых английских слов.",
    "🎵 Послушай новую музыку.",
    "😊 Сделай кому-нибудь приятный комплимент.",
    "📖 Узнай что-нибудь новое сегодня.",
    "🎨 Попробуй заняться творчеством.",
    "🌳 Проведи немного времени на природе."
]

# Список шуток
jokes = [
    "Почему программисты не любят природу? Там слишком много багов! 😂",
    "Что делает программист, когда ему скучно? Ищет баги!",
    "Почему компьютер замёрз? Потому что оставили Windows открытым!",
    "Программист — это человек, который решает проблемы, о которых ты не знал."
]


# Команда /start
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = (
        "👋 Привет! Добро пожаловать в бот заданий!\n\n"
        "🎯 Я помогу сделать твой день интереснее и продуктивнее.\n\n"
        "Каждый день ты можешь получать случайное задание.\n\n"
        "✨ Начни с маленьких шагов!\n\n"
        "Используй /help, чтобы посмотреть список команд."
    )

    # Создаём inline-кнопки
    keyboard = [
        [
            InlineKeyboardButton("О боте", callback_data="about"),
            InlineKeyboardButton("Шутка", callback_data="joke"),
            InlineKeyboardButton("Автор", callback_data="author")
        ]
    ]

    # Собираем клавиатуру
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветствие
    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


# Обработчик inline-кнопок
async def button_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    # Подтверждаем нажатие кнопки
    await query.answer()

    # Проверяем, какая кнопка нажата
    if query.data == "about":
        await query.message.reply_text(
            "🤖 Я бот заданий на каждый день!"
        )

    elif query.data == "joke":
        # Выбираем случайную шутку
        random_joke = random.choice(jokes)
        await query.message.reply_text(random_joke)

    elif query.data == "author":
        await query.message.reply_text(
            "👨‍💻 Автор бота: Ваше имя"
        )

    else:
        await query.message.reply_text(
            "Неизвестная кнопка!"
        )


# Команда /help
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = (
        "📋 Список доступных команд:\n\n"
        "/start — запустить бота\n"
        "/help — список команд\n"
        "/task — случайное задание\n"
        "/setprofile — создать или изменить профиль\n"
        "/profile — посмотреть сохранённый профиль\n"
        "/cancel — отменить создание профиля"
    )

    await update.message.reply_text(text)


# Команда /task
async def task(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Выбираем случайное задание
    random_task = random.choice(tasks)

    await update.message.reply_text(
        f"🎯 ТВОЁ ЗАДАНИЕ:\n\n{random_task}"
    )


# Начало создания профиля
async def setprofile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Привет! Давай создадим твой профиль.\n\n"
        "Как тебя зовут?"
    )

    return NAME


# Получение имени пользователя
async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Сохраняем имя временно
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Отлично! 🎨 Теперь напиши свой любимый цвет."
    )

    return COLOR


# Получение цвета и сохранение профиля
async def get_color(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Получаем ID пользователя
    user_id = str(update.effective_user.id)

    # Получаем имя из временных данных
    name = context.user_data["name"]

    # Получаем цвет
    color = update.message.text

    # Сохраняем профиль в словарь user_data
    user_data[user_id] = {
        "name": name,
        "color": color
    }

    # Сохраняем данные в JSON-файл
    save_users()

    await update.message.reply_text(
        f"✅ Профиль сохранён!\n\n"
        f"👤 Имя: {name}\n"
        f"🎨 Цвет: {color}"
    )

    # Завершаем диалог
    return ConversationHandler.END


# Команда /profile — показать профиль
async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Получаем ID пользователя
    user_id = str(update.effective_user.id)

    # Проверяем, есть ли профиль
    if user_id in user_data:
        name = user_data[user_id]["name"]
        color = user_data[user_id]["color"]

        await update.message.reply_text(
            f"👤 ТВОЙ ПРОФИЛЬ\n\n"
            f"Имя: {name}\n"
            f"Любимый цвет: {color}"
        )

    else:
        await update.message.reply_text(
            "Профиль ещё не создан.\n"
            "Используй команду /setprofile."
        )


# Отмена создания профиля
async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Создание профиля отменено."
    )

    return ConversationHandler.END


# Главная функция
def main():
    # Загружаем профили из JSON при запуске
    load_users()

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Создаём обработчик диалога профиля
    profile_handler = ConversationHandler(
        entry_points=[
            CommandHandler("setprofile", setprofile)
        ],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],
            COLOR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_color
                )
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # Регистрируем обработчики
    application.add_handler(profile_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("task", task))
    application.add_handler(CommandHandler("profile", profile))

    application.add_handler(
        CallbackQueryHandler(button_callback)
    )

    print("Бот успешно запущен!")

    # Запускаем бота
    application.run_polling()


# Запуск программы
if __name__ == "__main__":
    main()
