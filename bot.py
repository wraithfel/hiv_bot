from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен вашего бота
TOKEN = "8038332758:AAHINUOZ9SqvtJ-TacGOUF7eC4diVKi4Q_w"

file_path = "useful_links.txt"

# Чтение содержимого файла
with open(file_path, "r", encoding="utf-8") as file:  # encoding="utf-8" используется для поддержки кириллицы
    file_content = file.read()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data='welcome')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в бот ресторана \"Хачапури и Вино\"! Нажмите 'Начать', чтобы перейти к выбору раздела.",
        reply_markup=reply_markup
    )

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
            [InlineKeyboardButton("Специи и соусы", callback_data='spices_sauces')],
            [InlineKeyboardButton("Хинкали", callback_data='khinkali')],
            [InlineKeyboardButton("Закуски", callback_data='appetizers')],
            [InlineKeyboardButton("Салаты", callback_data='salads')],
            [InlineKeyboardButton("Супы", callback_data='soups')],
            [InlineKeyboardButton("Хачапури", callback_data='khachapuri')],
            [InlineKeyboardButton("Горячее", callback_data='main_dishes')],
            [InlineKeyboardButton("Завтраки", callback_data='breakfast')],
            [InlineKeyboardButton("Десерты", callback_data='desserts')],
            [InlineKeyboardButton("Назад", callback_data='welcome')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите раздел основного меню:", reply_markup=reply_markup)
    elif query.data == 'spices_sauces':
        keyboard = [
            [InlineKeyboardButton("Аджика", callback_data='adjika')],
            [InlineKeyboardButton("Сванская соль", callback_data='svansalt')],
            [InlineKeyboardButton("Хмели-сунели", callback_data='khmeli_suneli')],
            [InlineKeyboardButton("Уцхо-сунели", callback_data='utscho_suneli')],
            [InlineKeyboardButton("Кахетинское масло", callback_data='kah_oil')],
            [InlineKeyboardButton("Кондари", callback_data='kondari')],
            [InlineKeyboardButton("Аджика (50гр)", callback_data='adjika_50')],
            [InlineKeyboardButton("Ткемали (50гр)", callback_data='tkemali')],
            [InlineKeyboardButton("Сливочный соус с мятой (50гр)", callback_data='cream_mint')],
            [InlineKeyboardButton("Наршараб (50гр)", callback_data='narsharab')],
            [InlineKeyboardButton("Сацебели (50гр)", callback_data='satsebeli')],
            [InlineKeyboardButton("Сациви (50гр)", callback_data='satsivi')],
            [InlineKeyboardButton("Мацони", callback_data='matsoni')],
            [InlineKeyboardButton("Дзадзики", callback_data='tzatziki')],
            [InlineKeyboardButton("Назад", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите специю или соус:", reply_markup=reply_markup)
    elif query.data in [
        'adjika', 'svansalt', 'khmeli_suneli', 'utscho_suneli',
        'kah_oil', 'kondari', 'adjika_50', 'tkemali', 'cream_mint',
        'narsharab', 'satsebeli', 'satsivi', 'matsoni', 'tzatziki'
    ]:
        item_name = {
            'adjika': "Аджика",
            'svansalt': "Сванская соль",
            'khmeli_suneli': "Хмели-сунели",
            'utscho_suneli': "Уцхо-сунели",
            'kah_oil': "Кахетинское масло",
            'kondari': "Кондари",
            'adjika_50': "Аджика (50гр)",
            'tkemali': "Ткемали (50гр)",
            'cream_mint': "Сливочный соус с мятой (50гр)",
            'narsharab': "Наршараб (50гр)",
            'satsebeli': "Сацебели (50гр)",
            'satsivi': "Сациви (50гр)",
            'matsoni': "Мацони",
            'tzatziki': "Дзадзики"
        }
        await query.edit_message_text(f"Вы выбрали: *{item_name[query.data]}*.", parse_mode='Markdown')
    elif query.data == 'khinkali':
        await query.edit_message_text("Раздел *Хинкали* пока в разработке.")
    elif query.data == 'appetizers':
        await query.edit_message_text("Раздел *Закуски* пока в разработке.")
    elif query.data == 'salads':
        await query.edit_message_text("Раздел *Салаты* пока в разработке.")
    elif query.data == 'soups':
        await query.edit_message_text("Раздел *Супы* пока в разработке.")
    elif query.data == 'khachapuri':
        await query.edit_message_text("Раздел *Хачапури* пока в разработке.")
    elif query.data == 'main_dishes':
        await query.edit_message_text("Раздел *Горячее* пока в разработке.")
    elif query.data == 'breakfast':
        await query.edit_message_text("Раздел *Завтраки* пока в разработке.")
    elif query.data == 'desserts':
        await query.edit_message_text("Раздел *Десерты* пока в разработке.")
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

# Основная функция запуска бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
