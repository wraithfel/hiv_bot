from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8038332758:AAHINUOZ9SqvtJ-TacGOUF7eC4diVKi4Q_w"

# Основное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Обучение по меню", callback_data='menu_training')],
        [InlineKeyboardButton("Винная карта", callback_data='wine')],
        [InlineKeyboardButton("Тестирование", callback_data='test')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите раздел:", reply_markup=reply_markup)

# Обработка нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'menu_training':
        await query.edit_message_text("Раздел обучения по меню еще в разработке.")
    elif query.data == 'wine':
        await query.edit_message_text("Раздел обучения по винной карте еще в разработке.")
    elif query.data == 'test':
        await query.edit_message_text("Раздел тестирования еще в разработке.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
