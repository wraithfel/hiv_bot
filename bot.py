from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import psycopg2
import json
import openai

# Загрузка конфигурации базы данных
with open("db_config.json", "r", encoding="utf-8") as file:
    db_config = json.load(file)

# Загрузка токена бота и OpenAI API
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    TOKEN = config["BOT_TOKEN"]
    OPENAI_API_KEY = config["OPENAI_API_KEY"]

file_path = "useful_links.txt"

# Чтение содержимого файла
with open(file_path, "r", encoding="utf-8") as file:  # encoding="utf-8" используется для поддержки кириллицы
    file_content = file.read()

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

# Получение всех блюд из меню
def get_full_menu():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, category, description, photo_url, features, 
               ingredients, details, allergens, veg 
        FROM full_menu 
        ORDER BY id
    """)
    full_menu = [
        {
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "photo_url": row[4],
            "features": row[5],
            "ingredients": row[6],
            "details": row[7],
            "allergens": row[8],
            "veg": row[9]
        }
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return full_menu



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
def get_dish_by_id(dish_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, category, description, photo_url, features, 
               ingredients, details, allergens, veg 
        FROM full_menu 
        WHERE id = %s
        """,
        (dish_id,)
    )
    dish = cursor.fetchone()
    cursor.close()
    conn.close()
    return dish

def add_to_history(context, user_id, role, content):
    if 'conversation_history' not in context.user_data:
        context.user_data['conversation_history'] = []

    # Добавляем новый элемент в историю
    context.user_data['conversation_history'].append({"role": role, "content": content})

    # Ограничиваем историю до 5 элементов
    if len(context.user_data['conversation_history']) > 10:
        context.user_data['conversation_history'] = context.user_data['conversation_history'][-10:]

def parse_value(val):
    return val if val != "NaN" else "Отсутствуют"

# Генерация карточки блюда
async def send_dish_card(query, dish_data):
    if dish_data:
        # Извлекаем данные из записи о блюде
        (
            id, name, category, description, photo_url, features,
            ingredients, details, allergens, veg
        ) = dish_data

        # Формируем сообщение с карточкой блюда
        message = f"🍴 *{name}*\n"
        message += f"📂 Категория: {category}\n\n"

        if description:
            message += f"📖 *Описание:*\n{parse_value(description)}\n\n"
        if features:
            message += f"⭐ *Особенности:*\n{parse_value(features)}\n\n"
        if ingredients:
            message += f"📝 *Ингредиенты:*\n{parse_value(ingredients)}\n\n"
        if allergens:
            message += f"⚠️ *Аллергены:*\n{parse_value(allergens)}\n\n"
        if veg:
            message += f"🌱 *Подходит вегетарианцам/веганам:* {parse_value(veg)}\n\n"

        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='main_menu')],
            [InlineKeyboardButton("Задать вопрос по этому блюду", callback_data=f"ask_dish_{dish_data[0]}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с фото или текстом, если фото недоступно
        if photo_url:
            try:
                await query.message.reply_photo(
                    photo=photo_url,
                    caption=message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            except Exception as e:
                print(e)
                message += "\n🌐 Фото временно недоступно."
                await query.message.reply_text(
                    message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
        else:
            await query.message.reply_text(
                message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    else:
        await query.message.reply_text("Данные о выбранном блюде не найдены.")

# Генерация кнопок для категории
def get_buttons_for_category(category_name):
    dishes = get_dishes_by_category(category_name)
    buttons = [[InlineKeyboardButton(dish["name"], callback_data=f"dish_{dish['id']}")] for dish in dishes]
    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return buttons

# Обработчик основного меню
async def handle_main_menu(query):
    categories = get_categories()
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)] for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="welcome")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text:
        await query.edit_message_text("Выберите раздел основного меню:", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Выберите раздел основного меню:", reply_markup=reply_markup)

# Обработчик выбора категории
async def handle_category(query, category_name):

    keyboard = get_buttons_for_category(category_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text:
        await query.edit_message_text(f"Выберите блюдо из раздела '{category_name}':", reply_markup=reply_markup)
    else:
        await query.message.reply_text(f"Выберите блюдо из раздела '{category_name}':", reply_markup=reply_markup)

# Обработчик блюда
async def handle_dish(query, dish_id):
    dish_data = get_dish_by_id(dish_id)
    if dish_data:
        await send_dish_card(query, dish_data)
    else:
        await query.message.reply_text("Данные о выбранном блюде не найдены.", parse_mode='Markdown')

# Обработчик "Добро пожаловать"
async def handle_welcome(query):
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

# Оптимизированный button_handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == 'main_menu':
        await handle_main_menu(query)
    elif data in get_categories():
        await handle_category(query, data)
    elif data.startswith("dish_"):
        dish_id = int(data.split("_")[1])
        await handle_dish(query, dish_id)
    elif data.startswith("category_"):
        context.user_data['awaiting_question_for_dish'] = None
        category_name = data.split("_")[1]
        await query.message.reply_text("Вопросы по текущему блюду завершены. Вы можете выбрать другое блюдо.")
        await handle_category(query, category_name)
    elif data.startswith("ask_dish_"):
        dish_id = int(data.split("_")[2])  # Извлекаем ID блюда из callback_data
        dish_data = get_dish_by_id(dish_id)

        # Запрашиваем у пользователя вопрос по блюду
        await query.message.reply_text("Введите ваш вопрос по этому блюду:")
        context.user_data['awaiting_question_for_dish'] = dish_data
    elif data == 'welcome':
        await handle_welcome(query)
    elif query.data == 'links':
        try:
            keyboard = [
                [InlineKeyboardButton("Вернуться к выбору раздела", callback_data='welcome')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=file_content,
                parse_mode='Markdown',
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except Exception as e:
            await query.message.reply_text(f"Произошла ошибка: {str(e)}")
    else:
        await query.message.reply_text("Извините, я не могу обработать этот запрос. Попробуйте снова.")


# Обработчик текстового ввода для вопросов по блюду
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    history = context.user_data.get('conversation_history', [])

    # Добавляем новый запрос пользователя в историю
    add_to_history(context, update.effective_user.id, "user", user_message)

    # Проверка на вопрос по блюду
    if 'awaiting_question_for_dish' in context.user_data:
        dish_data = context.user_data['awaiting_question_for_dish']
        # Очистка данных о блюде
        full_menu = get_full_menu()

        # Добавляем данные о блюде в контекст
        prompt = f"История общения:{history}Блюдо: {dish_data[1]}\nВсе сведения о блюде: {dish_data[2:]}\nВот все меню ресторана, c его помощью можно давать советы и брать информацию, но ты можешь также использовать свои знания{full_menu}Вопрос: {user_message}"
        print(history)

        # Отправка запроса к OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Получение ответа от модели
            bot_response = response.choices[0].message.content

            add_to_history(context, update.effective_user.id, "assistant", bot_response)

            keyboard = [
                [InlineKeyboardButton("Завершить вопросы", callback_data=f'category_{dish_data[2]}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(bot_response, parse_mode='Markdown', reply_markup=reply_markup)

        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка при обработке запроса: {str(e)}")
    else:
        await update.message.reply_text("Пожалуйста, выберите блюдо, чтобы задать вопрос.")



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
