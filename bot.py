from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import psycopg2
from openai import OpenAI
import json
import openai
import pandas as pd

# Загрузка конфигурации базы данных
with open("db_config.json", "r", encoding="utf-8") as file:
    db_config = json.load(file)

# Загрузка токена бота и OpenAI API
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    TOKEN = config["BOT_TOKEN"]
    OPENAI_API_KEY = config["OPENAI_API_KEY"]

# Установка OpenAI API ключа
openai.api_key = OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Функция для подключения к базе данных
def connect_to_db():
    return psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )

# Получение всех категорий блюд
def get_categories():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM full_menu ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categories

# Получение всех блюд в категории
def get_dishes_by_category(category):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM full_menu WHERE category = %s ORDER BY id", (category,))
    dishes = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return dishes


# Получение данных о блюде по id
# Получение данных о блюде по id
def get_dish_by_id(dish_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, category, description, ingredients, photo_url, details FROM full_menu WHERE id = %s", (dish_id,)
    )
    dish = cursor.fetchone()
    cursor.close()
    conn.close()
    return dish

# Генерация карточки блюда
async def send_dish_card(query, dish_data):
    async def send_dish_card(query, dish_data):
        if dish_data:
            # Распаковка данных из запроса
            name, category, description, ingredients, photo_url, details, allergens, veg, features = dish_data

            # Начало формирования сообщения
            message = f"🍴 *{name}*\n"
            message += f"📂 Категория: {category}\n\n"

            # Добавляем данные только если они не NaN или пусты
            if pd.notna(description) and description.strip():
                message += f"📖 *Описание:*\n{description}\n\n"
            if pd.notna(ingredients) and ingredients.strip():
                message += f"📝 *Ингредиенты:*\n{ingredients}\n\n"
            if pd.notna(features) and features.strip():
                message += f"✨ *Особенности:*\n{features}\n\n"
            if pd.notna(allergens) and allergens.strip():
                message += f"⚠️ *Аллергены:*\n{allergens}\n\n"
            if pd.notna(veg) and veg.strip():
                message += f"🌱 *Можно ли веганам:*\n{veg}\n\n"
            if pd.notna(details) and details.strip():
                message += f"ℹ️ *Дополнительно:*\n{details}\n\n"

            # Кнопки для возврата в меню
            keyboard = [[InlineKeyboardButton("Назад", callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Проверяем наличие ссылки на фото
            if pd.notna(photo_url) and photo_url.strip():
                try:
                    await query.message.reply_photo(
                        photo=photo_url, caption=message, parse_mode='Markdown', reply_markup=reply_markup
                    )
                except Exception:
                    message += "\n🌐 Фото временно недоступно."
                    await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await query.message.reply_text("Данные о выбранном блюде не найдены.")

# Генерация кнопок для категории
def get_buttons_for_category(category_name):
    dishes = get_dishes_by_category(category_name)
    buttons = [[InlineKeyboardButton(dish["name"], callback_data=f"dish_{dish['id']}")] for dish in dishes]
    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return buttons

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'main_menu':
        categories = get_categories()
        keyboard = [
            [InlineKeyboardButton(category, callback_data=category)] for category in categories
        ]
        keyboard.append([InlineKeyboardButton("Задать вопрос", callback_data="ask_question")])
        keyboard.append([InlineKeyboardButton("Назад", callback_data="welcome")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.message.text:
            await query.edit_message_text("Выберите раздел основного меню:", reply_markup=reply_markup)
        else:
            await query.message.reply_text("Выберите раздел основного меню:", reply_markup=reply_markup)

    elif query.data in get_categories():
        category_name = query.data
        keyboard = get_buttons_for_category(category_name)
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.message.text:
            await query.edit_message_text(f"Выберите блюдо из раздела '{category_name}':", reply_markup=reply_markup)
        else:
            await query.message.reply_text(f"Выберите блюдо из раздела '{category_name}':", reply_markup=reply_markup)

    elif query.data.startswith("dish_"):
        dish_id = int(query.data.split("_")[1])
        dish_data = get_dish_by_id(dish_id)

        if dish_data:
            name, category, description, ingredients, photo_url, details, allergens, veg, features = dish_data
            message = f"*{name}*\n\n"
            if description:
                message += f"*Описание:* {description}\n\n"
            if ingredients:
                message += f"*Ингредиенты:* {ingredients}\n\n"
            if details:
                message += f"*Дополнительно:* {details}\n\n"

            keyboard = [[InlineKeyboardButton("Назад", callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if photo_url:
                try:
                    await query.message.reply_photo(photo=photo_url, caption=message, parse_mode='Markdown', reply_markup=reply_markup)
                except Exception:
                    await query.message.reply_text(message + "\n\n(Фото недоступно)", parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await query.message.reply_text("Данные о выбранном блюде не найдены.", parse_mode='Markdown')

    elif query.data == 'ask_question':
        await query.message.reply_text("Введите ваш вопрос, и я постараюсь ответить!")

        # Устанавливаем флаг для следующего ввода текста
        context.user_data['awaiting_question'] = True

    elif query.data == 'welcome':
        keyboard = [
            [InlineKeyboardButton("Основное меню", callback_data='main_menu')],
            [InlineKeyboardButton("Винная карта", callback_data='wine')],
            [InlineKeyboardButton("Особенности работы", callback_data='work_features')],
            [InlineKeyboardButton("Тестирование", callback_data='test')],
            [InlineKeyboardButton("Полезные ссылки", callback_data='links')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query.message.text:
            await query.edit_message_text("Выберите раздел:", reply_markup=reply_markup)
        else:
            await query.message.reply_text("Выберите раздел:", reply_markup=reply_markup)

    else:
        await query.message.reply_text("Извините, я не могу обработать этот запрос. Попробуйте снова.")

# Обработчик текстового ввода для вопросов
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Обрабатываю ваш запрос...")

    try:
        # Отправка запроса к OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Получение ответа от модели
        bot_response = response.choices[0].message.content
        await update.message.reply_text(bot_response)

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при обработке запроса: {str(e)}")


# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data="welcome")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в бот ресторана \"Хачапури и Вино\"! Нажмите 'Начать', чтобы перейти к выбору раздела.",
        reply_markup=reply_markup
    )

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    app.run_polling()

if __name__ == "__main__":
    main()
