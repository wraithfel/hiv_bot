from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import psycopg2
import json
import openai

file_path = "useful_links.txt"

# Загрузка конфигурации базы данных
with open("db_config.json", "r", encoding="utf-8") as file:
    db_config = json.load(file)

# Загрузка токена бота и OpenAI API
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    TOKEN = config["BOT_TOKEN"]
    OPENAI_API_KEY = config["OPENAI_API_KEY"]

# Чтение содержимого файла
with open(file_path, "r", encoding="utf-8") as file:  # encoding="utf-8" используется для поддержки кириллицы
    file_content = file.read()

# Установка OpenAI API ключа
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

def connect_to_db():
    return psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )

def export_menu_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL-запрос для извлечения всех данных из таблицы
    query = "SELECT * FROM full_menu"
    json_file_path = "menu_data.json"

    # Выполнение SQL-запроса
    cursor.execute(query)

    # Получение имен столбцов
    columns = [desc[0] for desc in cursor.description]

    # Формирование списка записей как словарей
    rows = cursor.fetchall()
    menu_data = [dict(zip(columns, row)) for row in rows]

    # Запись данных в JSON-файл
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(menu_data, json_file, ensure_ascii=False, indent=4)

    cursor.close()
    conn.close()

    print(f"Данные экспортированы в JSON-файл: {json_file_path}")
    return json_file_path


def create_vector_store():
    csv_file_path = export_menu_to_json()
    vector_store = client.beta.vector_stores.create(name="Menu Data Store")

    with open(csv_file_path, "rb") as file_stream:
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=[file_stream]
        )

    print("Vector Store создан с ID:", vector_store.id)
    return vector_store.id

def create_assistant_with_file_search(vector_store_id):
    assistant = client.beta.assistants.create(
        name="Restaurant Assistant",
        instructions="Ты — помощник для обучения стажеров-официантов ресторана. Отвечай на вопросы о меню, напитках и сервисе.",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )
    print("Ассистент создан с ID:", assistant.id)
    return assistant.id

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


# Генерация кнопок для категории
def get_buttons_for_category(category_name):
    dishes = get_dishes_by_category(category_name)
    buttons = [[InlineKeyboardButton(dish["name"], callback_data=f"dish_{dish['id']}")] for dish in dishes]
    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return buttons

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
        await query.edit_message_text(f"Выберите блюдо из раздела *{category_name}*:", parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await query.message.reply_text(f"Выберите блюдо из раздела *{category_name}*:", parse_mode='Markdown', reply_markup=reply_markup)

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

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    history = context.user_data.get('conversation_history', [])

    # Добавляем новый запрос пользователя в историю
    add_to_history(context, update.effective_user.id, "user", user_message)

    # Проверка, что есть активное блюдо
    if 'awaiting_question_for_dish' in context.user_data:
        dish_data = context.user_data['awaiting_question_for_dish']

        # Формируем запрос для ассистента
        user_prompt = f"Вопрос о блюде: {dish_data[1]}. {user_message} История общения:{history}"

        try:
            waiting_message = await update.message.reply_text(
                "⏳ Обработка запроса, пожалуйста, подождите..."
            )
            # Создаем поток
            thread = client.beta.threads.create(
                messages=[{"role": "user", "content": user_prompt}]
            )

            # Запускаем выполнение и ждем завершения
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id="asst_LQj1hbyuW3qwMhxO4ueLzg7x"
            )

            # Получаем список сообщений из выполнения
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            # Обрабатываем первое сообщение
            if messages:
                message_content = messages[0].content[0].text.value
                response_text = (
                    f"{message_content}\n\n"
                    "Вы можете задать следующий вопрос или нажать кнопку *Завершить вопросы*."
                )

                add_to_history(context, update.effective_user.id, "assistant", message_content)

                # Отправляем ответ пользователю
                keyboard = [
                    [InlineKeyboardButton("Завершить вопросы", callback_data=f'category_{dish_data[2]}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await waiting_message.edit_text(response_text, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await update.message.reply_text("К сожалению, я не смог получить ответ.")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")
    else:
        await update.message.reply_text("Пожалуйста, выберите блюдо для вопроса.")

# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data="welcome")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🍷 Добро пожаловать в бот ресторана *Хачапури и Вино*! 🍴\n\n"
        "👉 Нажмите *Начать*, чтобы перейти к выбору раздела!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Запуск бота
def main():
    # Создаем Vector Store и ассистента
    #vector_store_id = create_vector_store()
    #assistant_id = create_assistant_with_file_search(vector_store_id)'''

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    app.run_polling()

if __name__ == "__main__":
    main()
