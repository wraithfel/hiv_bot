from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from menu import MENU_DATA
import json


with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["BOT_TOKEN"]

file_path = "useful_links.txt"

# Чтение содержимого файла
with open(file_path, "r", encoding="utf-8") as file:  # encoding="utf-8" используется для поддержки кириллицы
    file_content = file.read()

# Токен вашего бота
TOKEN = "8038332758:AAHINUOZ9SqvtJ-TacGOUF7eC4diVKi4Q_w"



# Генерация кнопок для категории
def get_buttons_for_category(category_name):
    dishes = MENU_DATA.get(category_name, [])
    buttons = [[InlineKeyboardButton(name, callback_data=callback_data)] for callback_data, name in dishes]
    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return buttons

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'welcome':
        keyboard = [
            [InlineKeyboardButton("Основное меню", callback_data='main_menu')],
            [InlineKeyboardButton("Винная карта", callback_data='wine')],
            [InlineKeyboardButton("Особенности работы", callback_data='work_features')],
            [InlineKeyboardButton("Тестирование", callback_data='test')],
            [InlineKeyboardButton("Полезные ссылки", callback_data='links')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите раздел:", reply_markup=reply_markup)

    elif query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton(category, callback_data=category.lower().replace(" ", "_"))]
            for category in MENU_DATA.keys()
        ]
        keyboard.append([InlineKeyboardButton("Назад", callback_data="welcome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите раздел основного меню:", reply_markup=reply_markup)

    elif query.data in [category.lower().replace(" ", "_") for category in MENU_DATA.keys()]:
        category_name = next((name for name in MENU_DATA.keys() if name.lower().replace(" ", "_") == query.data), None)
        if category_name:
            keyboard = get_buttons_for_category(category_name)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"Выберите блюдо из раздела '{category_name}':", reply_markup=reply_markup)

    elif any(query.data == callback_data for dishes in MENU_DATA.values() for callback_data, _ in dishes):
        dish_name = next(
            (name for dishes in MENU_DATA.values() for callback_data, name in dishes if callback_data == query.data),
            None
        )
        if dish_name:
            await query.edit_message_text(f"Вы выбрали: *{dish_name}*.", parse_mode='Markdown')
    elif query.data == 'wine':
        await query.edit_message_text("Раздел *Винная карта* пока в разработке.")
    elif query.data == 'work_features':
        await query.edit_message_text("Раздел *Особенности работы* пока в разработке.")
    elif query.data == 'test':
        await query.edit_message_text("Раздел *Тестирование* пока в разработке.")
    elif query.data == 'links':
        keyboard = [[InlineKeyboardButton("Вернуться к выбору раздела", callback_data='welcome')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            file_content, disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


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
    app.run_polling()

if __name__ == "__main__":
    main()

