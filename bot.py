from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import re
import psycopg2
import json
import random
import openai
import os

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


def export_drinks_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL-запрос для извлечения всех данных из таблицы drinks
    query = "SELECT * FROM drinks"
    json_file_path = "drinks_data.json"

    try:
        # Выполнение SQL-запроса
        cursor.execute(query)

        # Получение имен столбцов
        columns = [desc[0] for desc in cursor.description]

        # Формирование списка записей как словарей
        rows = cursor.fetchall()
        drinks_data = [dict(zip(columns, row)) for row in rows]

        # Запись данных в JSON-файл
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(drinks_data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные экспортированы в JSON-файл: {json_file_path}")
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")
    finally:
        cursor.close()
        conn.close()

    return json_file_path

def export_drinks_questions_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM drinks_questions"
    json_file_path = "drinks_questions_data.json"

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        drinks_questions_data = [dict(zip(columns, row)) for row in rows]

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(drinks_questions_data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные из таблицы 'drinks_questions' экспортированы в JSON-файл: {json_file_path}")
    except Exception as e:
        print(f"Ошибка при экспорте данных из таблицы 'drinks_questions': {e}")
    finally:
        cursor.close()
        conn.close()

    return json_file_path


def export_faq_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM faq"
    json_file_path = "faq_data.json"

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        faq_data = [dict(zip(columns, row)) for row in rows]

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(faq_data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные из таблицы 'faq' экспортированы в JSON-файл: {json_file_path}")
    except Exception as e:
        print(f"Ошибка при экспорте данных из таблицы 'faq': {e}")
    finally:
        cursor.close()
        conn.close()

    return json_file_path


def export_test_ingredients_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM test_ingredients"
    json_file_path = "test_ingredients_data.json"

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        test_ingredients_data = [dict(zip(columns, row)) for row in rows]

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(test_ingredients_data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные из таблицы 'test_ingredients' экспортированы в JSON-файл: {json_file_path}")
    except Exception as e:
        print(f"Ошибка при экспорте данных из таблицы 'test_ingredients': {e}")
    finally:
        cursor.close()
        conn.close()

    return json_file_path


def export_work_features_questions_to_json():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM work_features_questions"
    json_file_path = "work_features_questions_data.json"

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        work_features_questions_data = [dict(zip(columns, row)) for row in rows]

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(work_features_questions_data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные из таблицы 'work_features_questions' экспортированы в JSON-файл: {json_file_path}")
    except Exception as e:
        print(f"Ошибка при экспорте данных из таблицы 'work_features_questions': {e}")
    finally:
        cursor.close()
        conn.close()

    return json_file_path



def clean_chatgpt_response(response: str) -> str:
    cleaned_response = re.sub(r"【\d+(?::\d+)?†source】", "", response)
    return cleaned_response.strip()


def create_vector_store_with_menu_and_drinks():
    # Экспорт данных о меню и напитках в JSON-файлы
    menu_file_path = export_menu_to_json()
    drinks_file_path = export_drinks_to_json()
    drinks_questions_file_path = export_drinks_questions_to_json()
    faq_file_path = export_faq_to_json()
    test_ingredients_file_path = export_test_ingredients_to_json()
    work_features_questions_file_path = export_work_features_questions_to_json()

    # Указываем пути к дополнительным файлам
    warnings_file_path = "warnings.txt"
    service_file_path = "service.txt"

    # Проверяем существование дополнительных файлов
    for fp in [warnings_file_path, service_file_path]:
        if not os.path.exists(fp):
            raise FileNotFoundError(f"Файл {file_path} не найден. Проверьте путь.")

    # Создаем Vector Store
    vector_store = client.beta.vector_stores.create(name="Menu, Drinks, and Service Data Store")

    # Загружаем все файлы в Vector Store

    file_paths = [menu_file_path, drinks_file_path, warnings_file_path, service_file_path, drinks_questions_file_path,
                  faq_file_path, test_ingredients_file_path, work_features_questions_file_path]

    file_streams = [open(path, "rb") for path in file_paths]

    try:
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )
    finally:
        # Закрываем открытые файловые потоки
        for stream in file_streams:
            stream.close()

    print("Vector Store создан с ID:", vector_store.id)
    print("Статус загрузки:", file_batch.status)
    print("Количество загруженных файлов:", file_batch.file_counts)
    return vector_store.id


def create_assistant_with_combined_file_search(vector_store_id):
    assistant = client.beta.assistants.create(
        name="Restaurant Assistant",
        instructions=(
            "Ты — ассистент ресторана. Отвечай на вопросы, связанные с ресторанной тематикой, а также на общие вопросы, "
            "которые могут быть связаны с работой ресторана, обслуживанием, меню, напитками или сервисом. "
            "Если вопрос не относится к ресторанной тематике (например, 'Какая погода сегодня?'), вежливо попроси задать вопрос по теме. "
            "Будь лояльным к вопросам, которые могут быть связаны с ресторанной тематикой, даже если они сформулированы не строго. "
            "Если в данных нет конкретного комментария о том, что можно сделать с блюдом (например, изменить тесто, убрать соус или специи),"
            "В первую очередь используй данные из подключенных файлов, если ничего не нашел - из своей базы знаний"
            "отвечай, что это невозможно, так как в нашем ресторане так блюдо не подают. "
            "Все соусы и специи — цельные заготовки, их нельзя изменять. Если пользователь спрашивает о такой возможности, отвечай, что это не предусмотрено. "
            "Будь строг в своих ответах, когда речь идёт о соблюдении установленных стандартов ресторана, но проявляй гибкость в коммуникации, чтобы пользователь чувствовал себя комфортно."
        ),

    model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    print("Ассистент создан с ID:", assistant.id)
    return assistant.id

def get_random_work_features_general(n=3):
    conn = connect_to_db()
    cursor = conn.cursor()
    # Запрашиваем больше, чем нужно, чтобы обеспечить разнообразие
    cursor.execute("SELECT question, answer, explanation FROM work_features_questions ORDER BY RANDOM() LIMIT %s", (n * 2,))
    raw = cursor.fetchall()
    cursor.close()
    conn.close()
    unique = list({(q[0], q[1], q[2]) for q in raw})
    random.shuffle(unique)
    selected = unique[:n]
    # Добавляем тип вопроса "work"
    return [{"question": q[0], "answer": q[1], "explanation": q[2], "type": "work"} for q in selected]


def get_random_menu_questions_general(n=6):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer, explanation FROM faq ORDER BY RANDOM() LIMIT %s", (n * 2,))
    raw = cursor.fetchall()
    cursor.close()
    conn.close()
    unique = list({(q[0], q[1], q[2], q[3]) for q in raw})
    random.shuffle(unique)
    selected = unique[:n]
    # Добавляем тип вопроса "menu"
    return [{
        "id": q[0],
        "question": q[1],
        "answer": q[2],
        "explanation": q[3],
        "type": "menu"
    } for q in selected]


def get_random_drink_questions_general(n=6):
    conn = connect_to_db()
    cursor = conn.cursor()
    # Здесь не фильтруем по категории – берем вопросы из всей таблицы
    cursor.execute("SELECT id, question, answer, explanation FROM drinks_questions ORDER BY RANDOM() LIMIT %s", (n * 2,))
    raw = cursor.fetchall()
    cursor.close()
    conn.close()
    random.shuffle(raw)
    selected = raw[:n]
    # Добавляем тип вопроса "drink"
    return [{"id": q[0], "question": q[1], "answer": q[2], "explanation": q[3], "type": "drink"} for q in selected]


async def handle_test_general(query, context):
    work_q = get_random_work_features_general(3)
    menu_q = get_random_menu_questions_general(6)
    drink_q = get_random_drink_questions_general(6)

    all_questions = work_q + menu_q + drink_q
    random.shuffle(all_questions)

    context.user_data['test_general'] = {
        "questions": all_questions,
        "current_index": 0,
        "score": 0
    }
    context.user_data['test_general_in_progress'] = True
    await send_next_general_question(query, context)

async def send_next_general_question(query, context):
    test = context.user_data.get('test_general')
    if not test or test["current_index"] >= len(test["questions"]):
        score = test["score"]
        total = len(test["questions"])
        context.user_data.pop("test_general_in_progress", None)
        context.user_data.pop("test_general", None)
        await query.message.reply_text(
            f"🎉 Общий тест завершён! Вы набрали *{score}/{total}* баллов.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="test")]])
        )
        return

    current_question = test["questions"][test["current_index"]]
    context.user_data["current_general_question"] = current_question
    await query.message.reply_text(
        f"❓ Вопрос {test['current_index'] + 1}:\n{current_question['question']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Завершить тест", callback_data="cancel_test")]
        ])
    )
async def handle_general_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    test = context.user_data.get('test_general')
    current_question = context.user_data.get('current_general_question')

    if not test or not current_question:
        await update.message.reply_text("❌ Тестирование неактивно.")
        return

    user_prompt = (
        "Ты — мой дружелюбный наставник. Оцени мой ответ максимально лояльно, "
        "с учетом смысла и ключевых слов, а не точного совпадения текста.\n\n"
        f"📌 Вопрос: {current_question['question']}\n"
        f"✍️ Мой ответ: {user_message}\n"
        f"✅ Верный ответ: {current_question['answer']}\n"
        f"💡 Дополнительное пояснение: {current_question['explanation']}\n\n"
        "Как оценивать:\n"
        "- Если ответ близок по смыслу к верному — напиши 'правильно', но всегда рассказывай полный вариант"
        " ответа с пояснением\n"
        "- Если ответ неверный — напиши 'неправильно' с комментариями\n"
    )

    try:
        waiting_message = await update.message.reply_text("⏳ Проверяю ваш ответ, подождите...")
        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU"
        )
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        if messages:
            assistant_response = clean_chatgpt_response(messages[0].content[0].text.value)
            await waiting_message.edit_text(f"💬 {assistant_response}", parse_mode="Markdown")
            # Простейшая логика: если в ответе встречается слово "правильно", засчитываем балл
            if "правильно" in assistant_response.lower() and "неправильно" not in assistant_response.lower():
                test["score"] += 1

            test["current_index"] += 1
            await send_next_general_question(update, context)
        else:
            await update.message.reply_text("К сожалению, я не смог проверить ваш ответ. Попробуйте снова.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


#выбираем рандомные вопросы для особенностей работы
def get_random_questions():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Получаем больше вопросов, чем нужно (например, 10 вместо 5), чтобы гарантировать разнообразие
    cursor.execute("SELECT question, answer, explanation FROM work_features_questions ORDER BY RANDOM() LIMIT 10")
    raw_questions = cursor.fetchall()

    cursor.close()
    conn.close()

    # Используем множество, чтобы убрать дубликаты
    unique_questions = list({(q[0], q[1], q[2]) for q in raw_questions})

    # Перемешиваем и берем 5 случайных вопросов
    random.shuffle(unique_questions)
    selected_questions = unique_questions[:5]

    return [{"question": q[0], "correct_answer": q[1], "explanation": q[2]} for q in selected_questions]


async def handle_test_drinks(query):
    """Меню выбора категории для тестирования по напиткам"""
    keyboard = [
        [InlineKeyboardButton("🍷 Красные вина", callback_data="test_drink_red")],
        [InlineKeyboardButton("🍾 Белые вина", callback_data="test_drink_white")],
        [InlineKeyboardButton("🥂 Остальные вина", callback_data="test_drink_wine")],
        [InlineKeyboardButton("🍹 Другие напитки", callback_data="test_drink_other")],
        [InlineKeyboardButton("🔙 Назад", callback_data="test")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите категорию напитков для тестирования:", reply_markup=reply_markup)


def get_random_drink_questions(category):
    """Выбор случайных вопросов по напиткам с учётом категории"""
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
        SELECT id, question, answer, explanation FROM drinks_questions
        WHERE category = %s
        ORDER BY RANDOM() LIMIT 7
    """
    cursor.execute(query, (category,))
    raw_questions = cursor.fetchall()
    cursor.close()
    conn.close()

    if not raw_questions:
        return []

    random.shuffle(raw_questions)
    return [{"id": q[0], "question": q[1], "answer": q[2], "explanation": q[3]} for q in raw_questions]

async def handle_test_drink_category(query, category, context):
    """Обработчик выбора категории напитков для тестирования"""

    category_map = {
        "red": "Красные вина",
        "white": "Белые вина",
        "wine": "Остальные вина",
        "other": "Другие напитки"
    }
    category = category_map[category]
    questions = get_random_drink_questions(category)

    if not questions:
        await query.message.reply_text("❌ В этой категории пока нет вопросов.")
        return

    context.user_data['test_drinks'] = {
        "questions": questions,
        "current_index": 0,
        "score": 0
    }

    context.user_data['test_drinks_in_progress'] = True
    await send_next_drink_question(query, context)

async def send_next_drink_question(query, context):
    """Отправка следующего вопроса по напиткам"""
    test = context.user_data.get('test_drinks')

    if not test or test["current_index"] >= len(test["questions"]):
        score = test["score"]
        total = len(test["questions"])
        context.user_data.pop("test_drinks_in_progress", None)
        context.user_data.pop("test_drinks", None)

        await query.message.reply_text(
            f"🎉 Тест по напиткам завершён! Вы набрали *{score}/{total}* баллов.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="test")]])
        )
        return

    current_question = test["questions"][test["current_index"]]
    context.user_data["current_drink_question"] = current_question

    await query.message.reply_text(
        f"❓ Вопрос {test['current_index'] + 1}:\n{current_question['question']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Завершить тест", callback_data="cancel_test")]
        ])
    )

async def handle_drink_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ответа пользователя в тесте по напиткам"""
    user_message = update.message.text.strip()
    test = context.user_data.get('test_drinks')
    current_question = context.user_data.get('current_drink_question')

    if not test or not current_question:
        await update.message.reply_text("❌ Тестирование неактивно.")
        return

    user_prompt = (
        f"Ты — мой дружелюбный наставник, помогающий разбираться в напитках ресторана Хачапури и Вино. "
        f"Оцени мой ответ **максимально лояльно**, учитывая **смысл** и **ключевые слова**,"
        f" а не точное совпадение текста.\n\n"
        f"📌 Вопрос: {current_question['question']}\n"
        f"✍️ Мой ответ: {user_message}\n"
        f"✅ Верный ответ: {current_question['answer']}\n"
        f"💡 Дополнительное пояснение (используй как совет, а не обязательную часть ответа): {current_question['explanation']}\n\n"
        f"🤖 Как оценивать:\n"
        f"- Если ответ **близок по смыслу** к верному — засчитывай **✅ Правильно!**\n"
        f"- Если ответ **верный, но содержит лишние детали** — тоже **✅ Правильно!**, просто уточни, что можно сказать короче\n"
        f"- Если ответ **ошибочный**, мягко объясни, что исправить, и напиши **❌ Пока неправильно**\n"
        f"- Если ответ верный, но можно дополнить, используй пояснение как дополнительный факт\n"
    )

    try:
        waiting_message = await update.message.reply_text("⏳ Проверяю ваш ответ, подождите...")

        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,
                                                       assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU")
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        if messages:
            assistant_response = clean_chatgpt_response(messages[0].content[0].text.value)
            await waiting_message.edit_text(f"💬 {assistant_response}", parse_mode="Markdown")

            if "правильно" in assistant_response.lower() and "неправильно" not in assistant_response.lower():
                test["score"] += 1

            test["current_index"] += 1
            await send_next_drink_question(update, context)
        else:
            await update.message.reply_text("К сожалению, я не смог проверить ваш ответ. Попробуйте снова.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

# Обработчик для кнопки "Особенности работы"
async def handle_work_features_test(query, context):
    # Генерация теста
    questions = get_random_questions()

    # Сохраняем тест в контексте
    context.user_data['current_test'] = {
        "questions": questions,
        "current_index": 0,
        "score": 0
    }

    context.user_data['test_in_progress'] = True

    # Отправляем первый вопрос
    await send_next_question(query, context)


async def send_next_question(query, context):
    test = context.user_data.get('current_test')

    if not test or test["current_index"] >= len(test["questions"]):
        # Завершаем тест, если вопросы закончились
        score = test["score"]
        total = len(test["questions"])
        keys_to_remove = ['test_in_progress', 'current_test', 'current_question']
        for key in keys_to_remove:
            context.user_data.pop(key, None)
        await query.message.reply_text(
            f"🎉 Тест завершён! Вы набрали *{score}/{total}* баллов.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="test")]])
        )
        return

    # Получаем текущий вопрос
    current_question = test["questions"][test["current_index"]]
    context.user_data["current_question"] = current_question
    print(current_question)

    # Отправляем вопрос пользователю
    await query.message.reply_text(
        f"❓ Вопрос {test['current_index'] + 1}:\n{current_question['question']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Завершить тест", callback_data="cancel_test")]
        ])
    )


# Обработчик кнопки "Завершить тест"
async def handle_cancel_test(query, context):
    # Завершаем текущий тест
    keys_to_remove = ['test_in_progress', 'current_test', 'current_question', 'test_menu_in_progress',
                      'test_drinks_in_progress', 'test_general_in_progress' ]
    for key in keys_to_remove:
        context.user_data.pop(key, None)

    # Сообщаем пользователю, что тест завершен
    await query.message.reply_text(
        "Вы завершили тест досрочно. Вы можете вернуться в раздел тестирования.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Вернуться", callback_data="test")]])
    )


async def handle_work_features_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ответы пользователей на тест по особенностям работы."""
    user_message = update.message.text.strip()

    # Проверяем, идет ли тестирование по особенностям работы
    test = context.user_data.get('current_test')
    current_question = context.user_data.get('current_question')

    if not test or not current_question:
        await update.message.reply_text("Тестирование неактивно.")
        return

    # Формируем промпт для ChatGPT
    user_prompt = (
        f"Ты — мой дружелюбный наставник, помогающий разбираться в работе официанта ресторана Хачапури и вино."
        f"Оцени мой ответ **максимально лояльно**, учитывая **смысл** и "
        f"**ключевые слова**, а не точное совпадение текста.\n\n"
        f"📌 Вопрос: {current_question['question']}\n"
        f"✍️ Мой ответ: {user_message}\n"
        f"✅ Верный ответ: {current_question['correct_answer']}\n"
        f"💡 Дополнительное пояснение (используй как совет, а не обязательную часть ответа):"
        f" {current_question['explanation']}\n\n"
        f"🤖 Как оценивать:\n"
        f"- Если ответ **близок по смыслу** к верному — засчитывай **✅ Правильно!**\n"
        f"- Если ответ **верный, но содержит лишние детали** — тоже"
        f" **✅ Правильно!**, просто уточни, что можно сказать короче\n"
        f"- Если ответ **ошибочный**, мягко объясни, что исправить,"
        f" и напиши **❌ Пока неправильно**\n"
        f"- Если ответ верный, но можно дополнить, используй пояснение как дополнительный факт\n"
    )

    try:
        waiting_message = await update.message.reply_text("⏳ Проверяю ваш ответ, подождите...")

        # Отправляем запрос в ChatGPT
        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU")
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        # Получаем ответ ChatGPT
        if messages:
            assistant_response = clean_chatgpt_response(messages[0].content[0].text.value)
            await waiting_message.edit_text(f"💬 {assistant_response}", parse_mode="Markdown")

            # Оцениваем результат теста
            if "правильно" in assistant_response.lower() and "неправильно" not in assistant_response.lower():
                test["score"] += 1

            # Переходим к следующему вопросу
            test["current_index"] += 1
            await send_next_question(update, context)
        else:
            await update.message.reply_text("К сожалению, я не смог проверить ваш ответ. Попробуйте снова.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

def get_random_menu_questions():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Получаем больше вопросов, чем нужно (например, 12 вместо 7), чтобы гарантировать разнообразие
    cursor.execute("SELECT id, question, answer, explanation FROM faq ORDER BY RANDOM() LIMIT 12")
    raw_questions = cursor.fetchall()

    cursor.close()
    conn.close()

    # Используем set для удаления возможных дубликатов
    unique_questions = list({(q[0], q[1], q[2], q[3]) for q in raw_questions})

    # Перемешиваем список перед финальным выбором
    random.shuffle(unique_questions)

    # Выбираем 7 случайных вопросов
    selected_questions = unique_questions[:7]

    return [{
        "id": q[0],
        "question": q[1],
        "answer": q[2],
        "explanation": q[3]
    } for q in selected_questions]


async def handle_test_full_menu(query, context):
    questions = get_random_menu_questions()

    context.user_data['test_menu'] = {
        "questions": questions,
        "current_index": 0,
        "score": 0
    }

    context.user_data['test_menu_in_progress'] = True
    await send_next_menu_question(query, context)


async def send_next_menu_question(query, context):
    test = context.user_data.get('test_menu')
    print(test)

    if not test or test["current_index"] >= len(test["questions"]):
        score = test["score"]
        total = len(test["questions"])
        context.user_data.pop("test_menu_in_progress", None)
        context.user_data.pop("test_menu", None)

        await query.message.reply_text(
            f"🎉 Тест завершён! Вы набрали *{score}/{total}* баллов.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="test")]])
        )
        return

    current_question = test["questions"][test["current_index"]]
    context.user_data["current_menu_question"] = current_question

    await query.message.reply_text(
        f"❓ Вопрос {test['current_index'] + 1}: {current_question['question']}",
    parse_mode = "Markdown",
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Завершить тест", callback_data="cancel_test")]
    ])
    )

async def handle_menu_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text.strip()
        test = context.user_data.get('test_menu')
        current_question = context.user_data.get('current_menu_question')

        if not test or not current_question:
            await update.message.reply_text("Тестирование неактивно.")
            return

        user_prompt = (
            f"Ты — мой дружелюбный наставник, помогающий разбираться в меню ресторана Хачапури и Вино. "
            f"Оцени мой ответ **максимально лояльно**, учитывая **смысл** и **ключевые слова**,"
            f" а не точное совпадение текста.\n\n"
            f"📌 Вопрос: {current_question['question']}\n"
            f"✍️ Мой ответ: {user_message}\n"
            f"✅ Верный ответ: {current_question['answer']}\n"
            f"💡 Дополнительное пояснение (используй как совет, а не обязательную часть ответа) Эту часть знаешь ты"
            f" - она создана для твоего понимания:"
            f" {current_question['explanation']}\n\n"
            f"🤖 Как оценивать:\n"
            f"- Если ответ **близок по смыслу** к верному — засчитывай **✅ Правильно!**\n"
            f"- Если ответ **верный, но содержит лишние детали** — тоже"
            f" **✅ Правильно!**, просто уточни, что можно сказать короче\n"
            f"- Если ответ **ошибочный**, мягко объясни, что исправить, и напиши **❌ Пока неправильно**\n"
            f"- Если ответ верный, но можно дополнить, используй пояснение как дополнительный факт\n"
        )

        try:
            waiting_message = await update.message.reply_text("⏳ Проверяю ваш ответ, подождите...")

            thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,
                                                           assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU")
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            if messages:
                assistant_response = clean_chatgpt_response(messages[0].content[0].text.value)
                await waiting_message.edit_text(f"💬 {assistant_response}", parse_mode="Markdown")

                if "правильно" in assistant_response.lower() and "неправильно" not in assistant_response.lower():
                    test["score"] += 1

                test["current_index"] += 1
                await send_next_menu_question(update, context)
            else:
                await update.message.reply_text("К сожалению, я не смог проверить ваш ответ. Попробуйте снова.")

        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")
# Чтение текста из файла
def read_text_from_file(fp):
    try:
        with open(fp, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Файл с информацией не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}"


async def handle_test_menu(query):
    keyboard = [
        [InlineKeyboardButton("Основное меню", callback_data="test_main_menu")],
        [InlineKeyboardButton("Напитки", callback_data="test_drinks")],
        [InlineKeyboardButton("Особенности работы", callback_data="test_work_features")],
        [InlineKeyboardButton("Общий тест", callback_data="test_general")],
        [InlineKeyboardButton("Назад", callback_data="welcome")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите раздел для тестирования:", reply_markup=reply_markup)


async def handle_test_main_menu(query):
    keyboard = [
        [InlineKeyboardButton("Тестирование по составам", callback_data="test_compositions")],
        [InlineKeyboardButton("Тестирование по всему меню", callback_data="test_full_menu")],
        [InlineKeyboardButton("Назад", callback_data="test")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите тип тестирования для основного меню:", reply_markup=reply_markup)


# Обработчик для тестирования "по составам" — выбор категории
async def handle_test_compositions(query):
    categories = get_categories()  # Получение всех категорий
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f"test_compositions_{category}")] for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="test_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "📋 Выберите категорию для тестирования по составам:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_test_compositions_category(query, category_name):
    dishes = get_dishes_by_category(category_name)  # Получение блюд в категории
    if not dishes:
        await query.edit_message_text(
            f"🚫 В категории *{category_name}* нет доступных блюд.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="test_compositions")]])
        )
        return

    keyboard = [
        [InlineKeyboardButton(dish["name"], callback_data=f"test_composition_dish_{dish['id']}")] for dish in dishes
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="test_compositions")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"📋 Выберите блюдо из категории *{category_name}* для проверки состава:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def get_dish_ingredients(dish_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT question, answer FROM test_ingredients WHERE id = %s",
        (dish_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {"name": row[0], "ingredients": row[1]}
    return None


async def handle_test_composition_dish(query, dish_id, context):
    dish_data = get_dish_ingredients(dish_id)
    d2 = get_dish_by_id(dish_id)

    if not dish_data:
        await query.message.reply_text("❌ Данные о составе блюда не найдены.")
        return

    context.user_data["test_composition_in_progress"] = True

    context.user_data["test_dish"] = {
        "dish_id": dish_id,
        "dish_name": dish_data["name"],
        "correct_ingredients": dish_data["ingredients"]
    }

    await query.message.reply_text(
        f"📋 Назовите полный состав блюда *{dish_data['name']}*.\n"
        "Перечислите все ингредиенты через запятую.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"test_compositions_{d2[2]}")]])
    )

async def handle_test_composition_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ответы пользователей на тест по составу блюд."""
    user_message = update.message.text.strip().lower()
    test_dish = context.user_data.get("test_dish")
    d2 = get_dish_by_id(test_dish['dish_id'])

    # Если нет данных о текущем блюде, просим пользователя выбрать снова
    if not test_dish:
        await update.message.reply_text("❌ Тестирование неактивно. Выберите блюдо заново.")
        return

    correct_ingredients = test_dish["correct_ingredients"].lower()

    # Формируем промпт для ChatGPT
    user_prompt = (
        f"Блюдо: {test_dish['dish_name']}\n"
        f"Ответ пользователя: {user_message}\n"
        f"Эталонный состав: {correct_ingredients}\n\n"
        f"Проанализируй ответ пользователя. Если есть ошибки, укажи, какие ингредиенты лишние(в случае если такие есть)"
        f" и какие отсутствуют (если пользователь не назвал какие-то ингредиенты)."
        f"Обратись к пользователю напрямую, как к другу, ведь ты его дружелюбный наставник,"
        f" избегая третьего лица. Вердикт: 'правильно' или 'неправильно'."
    )

    try:
        waiting_message = await update.message.reply_text("⏳ Проверяю ваш ответ, подождите...")

        # Отправляем запрос в ChatGPT
        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,
                                                       assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU")
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        if messages:
            assistant_response = clean_chatgpt_response(messages[0].content[0].text.value)
            keyboard = [[InlineKeyboardButton("🔙 Завершить", callback_data=f"test_compositions_{d2[2]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await waiting_message.edit_text(f"💬 {assistant_response}", parse_mode="Markdown", reply_markup=reply_markup)

            # Завершаем тест
            context.user_data.pop("test_dish", None)
            context.user_data.pop("test_composition_in_progress", None)
        else:
            await update.message.reply_text("К сожалению, я не смог проверить ваш ответ. Попробуйте снова.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


# Обработчики для смен
async def handle_morning_shift(query):
    text = read_text_from_file("morning_shift.txt")
    keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_day_shift(query):
    text = read_text_from_file("day_shift.txt")
    keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_evening_shift(query):
    # Читаем текст из файла
    with open("night_shift.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 3940] for i in range(0, len(text), 3940)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_iiko(query):
    # Читаем текст из файла
    with open("iiko.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 3940] for i in range(0, len(text), 3940)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_dating(query):
    # Читаем текст из файла
    with open("dating.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 3940] for i in range(0, len(text), 3940)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_base(query):
    # Читаем текст из файла
    with open("base.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 3907] for i in range(0, len(text), 3907)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)


async def handle_bring(query):
    # Читаем текст из файла
    with open("bring.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_wine(query):
    # Читаем текст из файла
    with open("wine.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4000 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)


async def handle_service(query):
    # Читаем текст из файла
    with open("service.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_instruction(query):
    # Читаем текст из файла
    with open("instruction.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="welcome")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_host(query):
    # Читаем текст из файла
    with open("host.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_delivery(query):
    # Читаем текст из файла
    with open("delivery.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_bar(query):
    # Читаем текст из файла
    with open("bar.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_special(query):
    # Читаем текст из файла
    with open("work.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # Разделяем текст на части не более 4096 символов
    parts = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    # Отправляем каждую часть текста как отдельное сообщение
    for i, part in enumerate(parts):
        keyboard = []
        # Добавляем кнопку "Назад" только к последнему сообщению
        if i == len(parts) - 1:
            keyboard = [[InlineKeyboardButton("Назад", callback_data="work_features")]]

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        # Если это первая часть, редактируем текущее сообщение
        if i == 0:
            await query.edit_message_text(part, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Если это последующие части, отправляем новые сообщения
            await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)


# Получение всех категорий блюд
def get_categories():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Выполняем запрос для получения всех категорий
    cursor.execute("SELECT DISTINCT category FROM full_menu")
    categories = [row[0] for row in cursor.fetchall()]

    # Определяем желаемый порядок категорий
    desired_order = [
        "Специи и соусы", "Закуски", "Салаты", "Супы", "Горячее",
        "Хачапури", "Хинкали", "Тесто", "Завтраки", "Десерты"
    ]

    # Сортируем категории на основе желаемого порядка
    # Категории, отсутствующие в желаемом порядке, остаются в конце
    categories = sorted(categories, key=lambda x: (desired_order.index(x) if x in desired_order else float('inf')))

    cursor.close()
    conn.close()
    return categories

def get_drink_categories():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM drinks ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categories
def get_subcategories_by_category(category):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT subcategory FROM drinks WHERE category = %s ORDER BY subcategory", (category,))
    subcategories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return subcategories

# Получение всех блюд в категории
def get_dishes_by_category(category):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM full_menu WHERE category = %s ORDER BY id", (category,))
    dishes = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return dishes

def get_drinks_by_subcategory(category, subcategory):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM drinks WHERE category = %s AND subcategory = %s ORDER BY id",
        (category, subcategory)
    )
    drinks = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return drinks


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

def get_drink_by_id(drink_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, category, description, photo_url, notes, 
               ingredients, aroma_profile, taste_profile, sugar_content, 
               producer, gastropair, subcategory
        FROM drinks 
        WHERE id = %s
        """,
        (drink_id,)
    )
    drink = cursor.fetchone()
    cursor.close()
    conn.close()
    return drink


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


async def send_drink_card(query, drink_data):
    if drink_data:
        # Извлекаем данные из записи о напитке
        (
            id, category, description, ingredients, photo_url, notes,
            aroma_profile, taste_profile, sugar_content, producer,
            gastropair, name, subcategory
        ) = drink_data

        # Формируем сообщение с карточкой напитка
        message = f"🍷 *{name}*\n"
        message += f"📂 Категория: {category}\n"
        if subcategory:
            message += f"🧾 Подкатегория: {subcategory}\n\n"

        if description:
            message += f"📖 *Описание:*\n{description}\n\n"
        if ingredients:
            message += f"📝 *Ингредиенты:*\n{ingredients}\n\n"
        if aroma_profile:
            message += f"👃 *Ароматический профиль:*\n{aroma_profile}\n\n"
        if taste_profile:
            message += f"👅 *Вкусовой профиль:*\n{taste_profile}\n\n"
        if sugar_content:
            message += f"🍬 *Стиль напитка:*\n{sugar_content}\n\n"
        if producer:
            message += f"🏭 *Производитель:*\n{producer}\n\n"
        if gastropair:
            message += f"🍽 *Гастропара:*\n{gastropair}\n\n"
        if notes:
            message += f"📝 *Примечания:*\n{notes}\n\n"

        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='drinks')],
            [InlineKeyboardButton("Задать вопрос по этому напитку", callback_data=f"ask_drink_{drink_data[0]}")]
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
        await query.message.reply_text("Данные о выбранном напитке не найдены.")


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

async def handle_take_order(query):
    keyboard = [
        [InlineKeyboardButton("Еда", callback_data='order_food')],
        [InlineKeyboardButton("Напитки", callback_data='order_drinks')],
        [InlineKeyboardButton("Назад", callback_data='welcome')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите категорию заказа:", reply_markup=reply_markup)

async def handle_order_food(query):
    categories = get_categories()
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f'order_category_{category}')] for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data='take_order')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем, совпадают ли текст и разметка с текущими
    current_text = query.message.text if query.message.text else ""
    new_text = "Выберите категорию еды:"

    if current_text != new_text or query.message.reply_markup != reply_markup:
        await query.edit_message_text(
            new_text,
            reply_markup=reply_markup
        )
    else:
        print("Сообщение не изменено. Запрос на редактирование пропущен.")


async def handle_order_drinks(query):
    categories = get_drink_categories()
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f'drink_order_category_{category}')] for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data='take_order')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите категорию напитков:", reply_markup=reply_markup)

async def handle_drink_order_category(query, category_name):
    subcategories = get_subcategories_by_category(category_name)
    keyboard = [
        [InlineKeyboardButton(subcategory, callback_data=f'drk_ord_sub_{category_name}_{subcategory}')]
        for subcategory in subcategories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data='order_drinks')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Выберите подкатегорию из категории *{category_name}*:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
async def handle_drink_order_subcategory(query, category_name, subcategory_name):
    drinks = get_drinks_by_subcategory(category_name, subcategory_name)
    keyboard = [
        [InlineKeyboardButton(drink["name"], callback_data=f"order_drink_{drink['id']}")] for drink in drinks
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"drink_order_category_{category_name}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем, можно ли редактировать сообщение
    if query.message.text:
        await query.edit_message_text(
            f"Напитки в подкатегории *{subcategory_name}*:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        # Если исходное сообщение пустое или не текстовое, отправляем новое сообщение
        await query.message.reply_text(
            f"Напитки в подкатегории *{subcategory_name}*:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )



async def handle_order_drink(query, drink_id):
    drink_data = get_drink_by_id(drink_id)
    if drink_data:
        # Извлекаем данные из записи о напитке
        (
            id, name, category, description, photo_url, notes,
            ingredients, aroma_profile, taste_profile, sugar_content,
            producer, gastropair, subcategory
        ) = drink_data

        # Формируем сообщение с карточкой напитка
        message = f"🍷 *{name}*\n"
        message += f"📂 Категория: {category}\n"
        if subcategory:
            message += f"🧾 Подкатегория: {subcategory}\n\n"

        if description:
            message += f"📖 *Описание:*\n{parse_value(description)}\n\n"
        if ingredients:
            message += f"📝 *Ингредиенты:*\n{parse_value(ingredients)}\n\n"
        if aroma_profile:
            message += f"👃 *Ароматический профиль:*\n{parse_value(aroma_profile)}\n\n"
        if taste_profile:
            message += f"👅 *Вкусовой профиль:*\n{parse_value(taste_profile)}\n\n"
        if sugar_content:
            message += f"🍬 *Стиль напитка:*\n{parse_value(sugar_content)}\n\n"
        if producer:
            message += f"🏭 *Производитель:*\n{parse_value(producer)}\n\n"
        if gastropair:
            message += f"🍽 *Гастропара:*\n{parse_value(gastropair)}\n\n"
        if notes:
            message += f"📝 *Примечания:*\n{parse_value(notes)}\n\n"

        keyboard = [
            [InlineKeyboardButton("Задать вопрос по напитку", callback_data=f"ask_order_drink_{drink_data[0]}")],
            [InlineKeyboardButton("Подтвердить выбор напитка", callback_data=f"drink_ok_{drink_data[0]}")],
            [InlineKeyboardButton("Назад к подкатегории", callback_data=f'drk_ord_sub_{category}_{subcategory}')]
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
        await query.message.reply_text("Данные о выбранном напитке не найдены.")

async def handle_drink_ok(query, drink_id, context):
    # Получаем данные о выбранном напитке
    drink_data = get_drink_by_id(drink_id)
    if not drink_data:
        await query.message.reply_text("Информация о выбранном напитке недоступна.")
        return

    # Сохраняем напиток в контексте
    context.user_data['current_drink'] = drink_data

    # Запрашиваем у пользователя количество напитка
    await query.message.reply_text(
        f"Вы выбрали *{drink_data[1]}*.\n\nВведите количество порций этого напитка:",
        parse_mode='Markdown'
    )


async def handle_order_category(query, category_name):
    dishes = get_dishes_by_category(category_name)
    buttons = [
        [InlineKeyboardButton(dish["name"], callback_data=f"order_dish_{dish['id']}")]
        for dish in dishes
    ]
    buttons.append([InlineKeyboardButton("Назад", callback_data=f'order_food')])
    reply_markup = InlineKeyboardMarkup(buttons)
    try:
        # Проверяем, можно ли редактировать сообщение
        if query.message.text:
            await query.edit_message_text(
                f"Выберите блюдо из категории *{category_name}*:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            # Если исходное сообщение пустое или не текстовое, отправляем новое
            await query.message.reply_text(
                f"Выберите блюдо из категории *{category_name}*:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    except Exception as e:
        await query.message.reply_text(
            "Произошла ошибка при обработке вашего запроса. Попробуйте снова."
        )


async def handle_order_dish(query, dish_id):
    dish_data = get_dish_by_id(dish_id)
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

        keyboard = [
            [InlineKeyboardButton("Задать вопрос по блюду", callback_data=f"ask_order_dish_{dish_data[0]}")],
            [InlineKeyboardButton("Подтвердить выбор блюда", callback_data=f"dish_ok_{dish_data[0]}")],
            [InlineKeyboardButton("Назад к блюдам категории", callback_data=f'order_category_{dish_data[2]}')]
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

async def handle_dish_ok(query, dish_id, context):
    # Получаем данные о выбранном блюде
    dish_data = get_dish_by_id(dish_id)
    if not dish_data:
        await query.message.reply_text("Информация о выбранном блюде недоступна.")
        return

    # Сохраняем блюдо в контексте
    context.user_data['current_dish'] = dish_data

    # Запрашиваем у пользователя количество блюда
    await query.message.reply_text(
        f"Вы выбрали *{dish_data[1]}*.\n\nВведите количество этого блюда:",
        parse_mode='Markdown'
    )

async def handle_finish_order(query, context):
    # Проверяем, есть ли оформленный заказ
    order = context.user_data.get('order', [])
    if not order:
        await query.message.reply_text(
            "Ваш заказ пуст. Пожалуйста, выберите блюда или напитки, прежде чем завершить заказ.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Вернуться к выбору еды", callback_data="order_food")],
                [InlineKeyboardButton("Вернуться к выбору напитков", callback_data="order_drinks")],
                [InlineKeyboardButton("Главное меню", callback_data="welcome")]
            ])
        )
        return

    # Формируем сообщение с заказом
    message = "📝 *Ваш заказ:*\n\n"

    for item in order:
        if 'dish' in item:  # Если это блюдо
            dish_name = item['dish'][1]
            quantity = item['quantity']
            if item['comment'] != None:
                comment = item['comment']
                message += f"🍽 *{dish_name}* x{quantity}\n  📋 Комментарий: {comment}\n\n"
            else:
                message += f"🍽 *{dish_name}* x{quantity}\n\n"

        elif 'drink' in item:  # Если это напиток
            drink_name = item['drink'][1]
            quantity = item['quantity']
            if item['comment'] != None:
                comment = item['comment']
                message += f"🍷 *{drink_name}* x{quantity}\n  📋 Комментарий: {comment}\n\n"
            else:
                message += f"🍷 *{drink_name}* x{quantity}\n\n"


    # Очищаем заказ из контекста
    context.user_data.pop('order', None)

    # Отправляем сообщение с итоговым заказом
    await query.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Вернуться в главное меню", callback_data="welcome")]
        ])
    )

async def handle_drinks_menu(query):
    categories = get_drink_categories()
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f"drink_category_{category}")] for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="welcome")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text:
        await query.edit_message_text("Выберите категорию напитков:", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Выберите категорию напитков:", reply_markup=reply_markup)

# Обработчик выбора категории
async def handle_category(query, category_name):
    keyboard = get_buttons_for_category(category_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text:
        await query.edit_message_text(f"Выберите блюдо из раздела *{category_name}*:", parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await query.message.reply_text(f"Выберите блюдо из раздела *{category_name}*:", parse_mode='Markdown', reply_markup=reply_markup)

async def handle_drink_category(query, category_name):
    subcategories = get_subcategories_by_category(category_name)

    # Перемещаем подкатегорию "Другое" в конец списка, если она есть
    if "Другое" in subcategories:
        subcategories.remove("Другое")
        subcategories.append("Другое")

    # Генерируем кнопки
    keyboard = [
        [InlineKeyboardButton(subcategory, callback_data=f"drink_subcategory_{category_name}_{subcategory}")]
        for subcategory in subcategories
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="drinks")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопками
    if query.message.text:
        await query.edit_message_text(
            f"Выберите подкатегорию из категории *{category_name}*:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await query.message.reply_text(
            f"Выберите подкатегорию из категории *{category_name}*:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )


async def handle_drink_subcategory(query, category_name, subcategory_name):
    drinks = get_drinks_by_subcategory(category_name, subcategory_name)
    keyboard = [
        [InlineKeyboardButton(drink["name"], callback_data=f"get_drink_{drink['id']}")] for drink in drinks
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"drink_category_{category_name}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text:
        await query.edit_message_text(f"Напитки в подкатегории *{subcategory_name}*:", parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await query.message.reply_text(f"Напитки в подкатегории *{subcategory_name}*:", parse_mode='Markdown', reply_markup=reply_markup)

# Обработчик блюда
async def handle_dish(query, dish_id):
    dish_data = get_dish_by_id(dish_id)
    if dish_data:
        await send_dish_card(query, dish_data)
    else:
        await query.message.reply_text("Данные о выбранном блюде не найдены.", parse_mode='Markdown')

async def handle_drink(query, drink_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, category, description, ingredients, photo_url, notes,
               aroma_profile, taste_profile, sugar_content, producer,
               gastropair, name, subcategory
        FROM drinks WHERE id = %s
        """,
        (drink_id,)
    )
    drink_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if drink_data:
        await send_drink_card(query, drink_data)
    else:
        await query.message.reply_text("Данные о выбранном напитке не найдены.", parse_mode='Markdown')


# Обработчик "Добро пожаловать"
async def handle_welcome(query):
    keyboard = [
        [InlineKeyboardButton("Основное меню", callback_data='main_menu')],
        [InlineKeyboardButton("Напитки", callback_data='drinks')],
        [InlineKeyboardButton("Полезная информация", callback_data='work_features')],
        [InlineKeyboardButton("Тестирование", callback_data='test')],
        [InlineKeyboardButton("Принять заказ", callback_data='take_order')],
        [InlineKeyboardButton("💬 Задать общий вопрос", callback_data='general_question')],
        [InlineKeyboardButton("Полезные ссылки", callback_data='links')],
        [InlineKeyboardButton("📖 Инструкция", callback_data="instruction")],
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
    elif data == "work_features":
        keyboard = [
            [InlineKeyboardButton("Утренняя смена", callback_data="work_morning")],
            [InlineKeyboardButton("Дневная смена", callback_data="work_day")],
            [InlineKeyboardButton("Вечерняя смена", callback_data="work_evening")],
            [InlineKeyboardButton("Знакомство с ХиВом", callback_data="work_dating")],
            [InlineKeyboardButton("Основы основ", callback_data="work_base")],
            [InlineKeyboardButton("Работа с iiko", callback_data="work_iiko")],
            [InlineKeyboardButton("Работа на раздаче", callback_data="work_bring")],
            [InlineKeyboardButton("Шаги сервиса", callback_data="work_service")],
            [InlineKeyboardButton("Хост", callback_data="work_host")],
            [InlineKeyboardButton("Работа с доставкой", callback_data="work_delivery")],
            [InlineKeyboardButton("О производстве вина", callback_data="work_wine")],
            [InlineKeyboardButton("Работа с баром", callback_data="work_bar")],
            [InlineKeyboardButton("Особые случаи", callback_data="work_special")],
            [InlineKeyboardButton("Назад", callback_data="welcome")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем новое сообщение, а не редактируем текущее
        await query.message.reply_text(
            "Выберите раздел, чтобы узнать подробности:",
            reply_markup=reply_markup
        )
    elif data == "work_morning":
        await handle_morning_shift(query)
    elif data == 'test':
        await handle_test_menu(query)
    elif data == 'instruction':
        await handle_instruction(query)
    elif data == "test_general":
        await handle_test_general(query, context)
    elif data == "test_drinks":
        await handle_test_drinks(query)
    elif data.startswith("test_drink_"):
        category = data.split("_")[2]
        await handle_test_drink_category(query, category, context)
    elif data == "test_main_menu":
        await handle_test_main_menu(query)
    elif data == "test_compositions":
        await handle_test_compositions(query)
    elif data.startswith("test_compositions_"):
        category_name = data.split("_", 2)[2]
        await handle_test_compositions_category(query, category_name)
    elif data.startswith("test_composition_dish_"):
        dish_id = int(data.split("_")[3])
        await handle_test_composition_dish(query, dish_id, context)
    elif data.startswith("test_full_menu"):
        await handle_test_full_menu(query, context)
    elif data == "test_work_features":
        await handle_work_features_test(query, context)
    elif data == "cancel_test":
        await handle_cancel_test(query, context)
    elif data == "work_day":
        await handle_day_shift(query)
    elif data == "work_evening":
        await handle_evening_shift(query)
    elif data == "work_iiko":
        await handle_iiko(query)
    elif data == "work_dating":
        await handle_dating(query)
    elif data == "work_service":
        await handle_service(query)
    elif data == "work_special":
        await handle_special(query)
    elif data == "work_base":
        await handle_base(query)
    elif data == "work_host":
        await handle_host(query)
    elif data == "work_wine":
        await handle_wine(query)
    elif data == "work_bar":
        await handle_bar(query)
    elif data == "work_delivery":
        await handle_delivery(query)
    elif data == "work_bring":
        await handle_bring(query)
    elif data in get_categories():
        await handle_category(query, data)
    elif data == 'take_order':
        await handle_take_order(query)
    elif data == "no_comment_dish":
        # Если нажата кнопка "Без комментария", переходим к обработке как текстового ввода

        # Получаем данные о текущем блюде и количестве
        current_dish = context.user_data.pop('current_dish', None)
        current_quantity = context.user_data.pop('current_quantity', None)

        if current_dish and current_quantity:
            # Сохраняем блюдо, количество и комментарий в заказ
            if 'order' not in context.user_data:
                context.user_data['order'] = []
            context.user_data['order'].append({
                "dish": current_dish,
                "quantity": current_quantity,
                "comment": None
            })

            # Уведомляем пользователя о добавлении блюда
            await query.message.reply_text(
                f"Блюдо *{current_dish[1]}* x{current_quantity} добавлено в заказ!\n"
                "Выберите следующее блюдо или завершите заказ.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Завершить заказ", callback_data="finish_order")],
                    [InlineKeyboardButton("Продолжить выбор", callback_data="take_order")],
                ])
            )
        else:
            await query.message.reply_text("Произошла ошибка: не удалось обработать заказ.")
        return
    elif data == "no_comment_drink":
        # Если нажата кнопка "Без комментария", переходим к обработке как текстового ввода

        # Получаем данные о текущем блюде и количестве
        current_drink = context.user_data.pop('current_drink', None)
        current_quantity = context.user_data.pop('current_quantity', None)

        if current_drink and current_quantity:
            # Сохраняем напиток, количество и комментарий в заказ
            if 'order' not in context.user_data:
                context.user_data['order'] = []
            context.user_data['order'].append({
                "drink": current_drink,
                "quantity": current_quantity,
                "comment": None
            })

            # Уведомляем пользователя о добавлении напитка
            await query.message.reply_text(
                f"Напиток *{current_drink[1]}* x{current_quantity} добавлен в заказ!\n"
                "Выберите следующий напиток или завершите заказ.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Завершить заказ", callback_data="finish_order")],
                    [InlineKeyboardButton("Продолжить выбор", callback_data="take_order")],
                ])
            )
        else:
            await query.message.reply_text("Произошла ошибка: не удалось обработать заказ.")
        return

    elif data == 'order_food':
        await handle_order_food(query)
    elif data.startswith('order_category_'):
        category_name = data.split('_')[2]
        await handle_order_category(query, category_name)
    elif data.startswith('order_dish_'):
        context.user_data.pop('awaiting_question_for_order_dish', None)
        dish_id = int(data.split('_')[2])
        await handle_order_dish(query, dish_id)
    elif data.startswith("ask_order_dish_"):
        dish_id = int(data.split("_")[3])  # Извлекаем ID блюда из callback_data
        dish_data = get_dish_by_id(dish_id)
        # Запрашиваем у пользователя вопрос по блюду
        await query.message.reply_text("Введите ваш вопрос по этому блюду:")
        context.user_data['awaiting_question_for_order_dish'] = dish_data

    elif data == 'order_drinks':
        await handle_order_drinks(query)
    elif data.startswith('drink_order_category_'):
        category_name = data.split('_')[3]
        await handle_drink_order_category(query, category_name)
    elif data.startswith('drk_ord_sub_'):
        _, _, _, category_name, subcategory_name = data.split('_')
        await handle_drink_order_subcategory(query, category_name, subcategory_name)
    elif data.startswith('order_drink_'):
        context.user_data.pop('awaiting_question_for_order_drink', None)
        drink_id = int(data.split('_')[2])
        await handle_order_drink(query, drink_id)
    elif data.startswith('drink_ok_'):
        drink_id = int(data.split('_')[2])
        await handle_drink_ok(query, drink_id, context)
    elif data.startswith("ask_order_drink_"):
        drink_id = int(data.split("_")[3])  # Извлекаем ID блюда из callback_data
        drink_data = get_drink_by_id(drink_id)
        # Запрашиваем у пользователя вопрос по блюду
        await query.message.reply_text("Введите ваш вопрос по этому блюду:")
        context.user_data['awaiting_question_for_order_drink'] = drink_data
    elif data.startswith("dish_ok_"):
        dish_id = int(data.split('_')[2])
        await handle_dish_ok(query, dish_id, context)
    elif data == "finish_order":
        await handle_finish_order(query, context)
    elif data == 'drinks':  # Главное меню напитков
        await handle_drinks_menu(query)
    elif data.startswith("drink_category_"):  # Выбор категории напитков
        category_name = data.split("_")[2]
        await handle_drink_category(query, category_name)
    elif data.startswith("drink_subcategory_"):  # Выбор подкатегории напитков
        _, _, category_name, subcategory_name = data.split("_")
        await handle_drink_subcategory(query, category_name, subcategory_name)
    elif data.startswith("get_drink_"):  # Выбор конкретного напитка
        drink_id = int(data.split("_")[2])
        await handle_drink(query, drink_id)
    elif data.startswith("dish_"):
        dish_id = int(data.split("_")[1])
        await handle_dish(query, dish_id)
    elif data.startswith("category_"):
        context.user_data.pop('awaiting_question_for_dish')
        category_name = data.split("_")[1]
        await query.message.reply_text("Вопросы по текущему блюду завершены. Вы можете выбрать другое блюдо.")
        await handle_category(query, category_name)
    elif data.startswith("back_drink_"):
        context.user_data.pop('awaiting_question_for_drink')
        category_name = data.split("_")[2]
        subcategory_name = data.split("_")[3]
        await query.message.reply_text("Вопросы по текущему напитку завершены. Вы можете выбрать другой напиток.")
        await handle_drink_subcategory(query, category_name, subcategory_name)
    elif data.startswith("ask_drink_"):  # Задать вопрос по напитку
        drink_id = int(data.split("_")[2])
        drink_data = get_drink_by_id(drink_id)

        if drink_data:
            context.user_data['awaiting_question_for_drink'] = drink_data
            await query.message.reply_text("Введите ваш вопрос по этому напитку:")
        else:
            await query.message.reply_text("Не удалось найти данные о выбранном напитке.")

    elif data.startswith("ask_dish_"):
        dish_id = int(data.split("_")[2])  # Извлекаем ID блюда из callback_data
        dish_data = get_dish_by_id(dish_id)
        # Запрашиваем у пользователя вопрос по блюду
        await query.message.reply_text("Введите ваш вопрос по этому блюду:")
        context.user_data['awaiting_question_for_dish'] = dish_data
    elif data == 'general_question':
        context.user_data['general_question_in_progress'] = True
        keyboard = [[InlineKeyboardButton("⏹ Прекратить общение", callback_data="stop_chat")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🗣 Вы можете задать любой вопрос. Я поддерживаю диалог и помню историю беседы.\n\n"
            "Когда захотите закончить разговор, нажмите кнопку *Прекратить общение*.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif data == "stop_chat":
        context.user_data.pop("general_question_in_progress", None)
        context.user_data.pop("conversation_history", None)  # Можно очищать историю для нового диалога

        await query.message.reply_text(
            "🔚 Общий диалог завершён. Вы можете вернуться в главное меню.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Главное меню", callback_data="welcome")]])
        )

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
    if context.user_data.get("test_general_in_progress"):
        await handle_general_test_answer(update, context)
        return

    elif context.user_data.get("test_composition_in_progress"):
        await handle_test_composition_answer(update, context)
        return

    elif context.user_data.get("test_menu_in_progress"):
        await handle_menu_test_answer(update, context)
        return

    elif context.user_data.get("test_in_progress"):
        await handle_work_features_answer(update, context)
        return

    elif context.user_data.get("test_drinks_in_progress"):
        await handle_drink_test_answer(update, context)
        return

    history = context.user_data.get('conversation_history', [])

    # Добавляем новый запрос пользователя в историю
    add_to_history(context, update.effective_user.id, "user", user_message)

    if context.user_data.get("general_question_in_progress"):

        # Формируем запрос для ChatGPT
        user_prompt = (
            "Ты — эксперт по ресторанному делу и обслуживанию, наставник официанта-стажера,"
            "твоя задача — помогать с вопросами со стороны официанта,"
            "связанными с меню (блюда, напитки), сервисом, работой официанта и всем, что входит в его обязанности."
            "Ты работаешь в ресторане 'Хачапури и Вино' и помогаешь разбираться в стандартах работы."
            "📌 Используй в первую очередь данные из подключенных файлов (меню, напитки, сервис). "
            "Не предлагай позиций, которых нет в нашем меню и напитках"
            "Если нужной информации там нет, используй свою базу знаний.\n\n"

            f"🔹 История диалога:\n{history}\n\n"
            f"🗣 Пользователь: {user_message}"
        )

        try:
            waiting_message = await update.message.reply_text("⏳ Думаю над ответом...")

            # Создаём поток и выполняем запрос
            thread = client.beta.threads.create(messages=[{"role": "user", "content": user_prompt}])
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,
                                                           assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU")
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            if messages:
                message_content = clean_chatgpt_response(messages[0].content[0].text.value)

                # Сохраняем ответ в историю
                add_to_history(context, update.effective_user.id, "assistant", message_content)

                keyboard = [[InlineKeyboardButton("⏹ Прекратить общение", callback_data="stop_chat")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await waiting_message.edit_text(f"💬 {message_content}", parse_mode="Markdown",
                                                reply_markup=reply_markup)
            else:
                await update.message.reply_text("К сожалению, я не смог получить ответ.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")
        return

    elif 'current_dish' in context.user_data and 'current_quantity' not in context.user_data:
        try:
            # Преобразуем ввод в число
            quantity = int(user_message)
            if quantity <= 0:
                await update.message.reply_text("Пожалуйста, введите положительное число.")
                return

            # Сохраняем количество
            context.user_data['current_quantity'] = quantity

            keyboard = [
                [InlineKeyboardButton("Без комментария", callback_data="no_comment_dish")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Добавьте комментарий к блюду (или нажмите 'Без комментария'):",
                reply_markup=reply_markup
            )
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное количество (число).")

        # Проверяем, ожидается ли ввод комментария
    elif 'current_dish' in context.user_data and 'current_quantity' in context.user_data:
        # Получаем данные о текущем блюде и количестве
        current_dish = context.user_data.pop('current_dish')
        current_quantity = context.user_data.pop('current_quantity')
        comment = user_message if user_message.strip().lower() != "без комментария" else "Без комментария"

        # Сохраняем блюдо, количество и комментарий в заказ
        if 'order' not in context.user_data:
            context.user_data['order'] = []
        context.user_data['order'].append({
            "dish": current_dish,
            "quantity": current_quantity,
            "comment": comment
        })

        # Уведомляем пользователя о добавлении блюда
        await update.message.reply_text(
            f"Блюдо *{current_dish[1]}* x{current_quantity} добавлено в заказ!\n"
            "Выберите следующее блюдо или завершите заказ.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Завершить заказ", callback_data="finish_order")],
                [InlineKeyboardButton("Продолжить выбор", callback_data="take_order"), ]
            ])
        )

    elif 'current_drink' in context.user_data and 'current_quantity' not in context.user_data:
        try:
            # Преобразуем ввод в число
            quantity = int(user_message)
            if quantity <= 0:
                await update.message.reply_text("Пожалуйста, введите положительное число.")
                return

            # Сохраняем количество
            context.user_data['current_quantity'] = quantity

            keyboard = [
                [InlineKeyboardButton("Без комментария", callback_data="no_comment_drink")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Добавьте комментарий к напитку (или нажмите 'Без комментария'):",
                reply_markup=reply_markup
            )
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное количество (число).")

    # Проверяем, ожидается ли ввод комментария
    elif 'current_drink' in context.user_data and 'current_quantity' in context.user_data:
        # Получаем данные о текущем напитке и количестве
        current_drink = context.user_data.pop('current_drink')
        current_quantity = context.user_data.pop('current_quantity')
        comment = user_message if user_message.strip().lower() != "без комментария" else "Без комментария"

        # Сохраняем напиток, количество и комментарий в заказ
        if 'order' not in context.user_data:
            context.user_data['order'] = []
        context.user_data['order'].append({
            "drink": current_drink,
            "quantity": current_quantity,
            "comment": comment
        })

        # Уведомляем пользователя о добавлении напитка
        await update.message.reply_text(
            f"Напиток *{current_drink[1]}* x{current_quantity} добавлен в заказ!\n"
            "Выберите следующий напиток или завершите заказ.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Завершить заказ", callback_data="finish_order")],
                [InlineKeyboardButton("Продолжить выбор", callback_data="take_order"), ]
            ])
        )

    # Проверка, что есть активное блюдо
    elif 'awaiting_question_for_dish' in context.user_data:
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
                thread_id=thread.id, assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU"
            )

            # Получаем список сообщений из выполнения
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            # Обрабатываем первое сообщение
            if messages:
                message_content = clean_chatgpt_response(messages[0].content[0].text.value)
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
    elif 'awaiting_question_for_drink' in context.user_data:
        drink_data = context.user_data['awaiting_question_for_drink']

        # Формируем запрос для ассистента
        user_prompt = f"Вопрос о напитке: {drink_data[1]}. {user_message} История общения: {history}"

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
                thread_id=thread.id, assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU"
            )

            # Получаем список сообщений из выполнения
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            # Обрабатываем первое сообщение
            if messages:
                message_content = clean_chatgpt_response(messages[0].content[0].text.value)
                response_text = (
                    f"{message_content}\n\n"
                    "Вы можете задать следующий вопрос или нажать кнопку *Завершить вопросы*."
                )

                add_to_history(context, update.effective_user.id, "assistant", message_content)

                # Отправляем ответ пользователю
                keyboard = [
                    [InlineKeyboardButton("Завершить вопросы", callback_data=f'back_drink_{drink_data[2]}_{drink_data[-1]}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await waiting_message.edit_text(response_text, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await update.message.reply_text("К сожалению, я не смог получить ответ.")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")
    elif 'awaiting_question_for_order_dish' in context.user_data:
        dish_data = context.user_data['awaiting_question_for_order_dish']
        print(dish_data)

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
                thread_id=thread.id, assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU"
            )

            # Получаем список сообщений из выполнения
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            # Обрабатываем первое сообщение
            if messages:
                message_content = clean_chatgpt_response(messages[0].content[0].text.value)
                response_text = (
                    f"{message_content}\n\n"
                    "Вы можете задать следующий вопрос или нажать кнопку *Завершить вопросы*."
                )

                add_to_history(context, update.effective_user.id, "assistant", message_content)

                # Отправляем ответ пользователю
                keyboard = [
                    [InlineKeyboardButton("Завершить вопросы", callback_data=f'order_dish_{dish_data[0]}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await waiting_message.edit_text(response_text, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await update.message.reply_text("К сожалению, я не смог получить ответ.")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")
    elif 'awaiting_question_for_order_drink' in context.user_data:
        drink_data = context.user_data['awaiting_question_for_order_drink']

        # Формируем запрос для ассистента
        user_prompt = f"Вопрос о напитке: {drink_data[1]}. {user_message} История общения:{history}"

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
                thread_id=thread.id, assistant_id="asst_35v1pLP2iy1MCdxvAZbPDviU"
            )

            # Получаем список сообщений из выполнения
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            # Обрабатываем первое сообщение
            if messages:
                message_content = clean_chatgpt_response(messages[0].content[0].text.value)
                response_text = (
                    f"{message_content}\n\n"
                    "Вы можете задать следующий вопрос или нажать кнопку *Завершить вопросы*."
                )

                add_to_history(context, update.effective_user.id, "assistant", message_content)

                # Отправляем ответ пользователю
                keyboard = [
                    [InlineKeyboardButton("Завершить вопросы", callback_data=f'order_drink_{drink_data[0]}')]
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
    keys_to_remove = [
        'test_in_progress',
        'test_menu_in_progress',
        'test_composition_in_progress',
        'current_test',
        'test_drinks_in_progress',
        'test_general_in_progress',
        'current_question',
        'current_drink_question',
        'current_menu_question',
    ]
    for key in keys_to_remove:
        context.user_data.pop(key, None)
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
    # Создаем Vector Store с данными меню и напитков
    #vector_store_id = create_vector_store_with_menu_and_drinks()

    # Создаем ассистента с доступом к этому Vector Store
    #assistant_id = create_assistant_with_combined_file_search(vector_store_id)

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    app.run_polling()


if __name__ == "__main__":
    main()
