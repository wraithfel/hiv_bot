from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8038332758:AAHINUOZ9SqvtJ-TacGOUF7eC4diVKi4Q_w"

# Стартовое сообщение с кнопкой "Начать"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data='welcome')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в бот ресторана \"Хачапури и Вино\"! Нажмите 'Начать', чтобы перейти к выбору раздела.", reply_markup=reply_markup)

# Главное меню
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Основное меню", callback_data='main_menu')],
        [InlineKeyboardButton("Винная карта", callback_data='wine')],
        [InlineKeyboardButton("Особенности работы", callback_data='work_features')],
        [InlineKeyboardButton("Тестирование", callback_data='test')],
        [InlineKeyboardButton("Полезные ссылки", callback_data='links')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("Выберите раздел:", reply_markup=reply_markup)

# Обработка разделов
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'main_menu':
        await query.edit_message_text("Раздел *Основное меню* пока в разработке.")
    elif query.data == 'wine':
        await query.edit_message_text("Раздел *Винная карта* пока в разработке.")
    elif query.data == 'work_features':
        await query.edit_message_text("Раздел *Особенности работы* пока в разработке.")
    elif query.data == 'test':
        await query.edit_message_text("Раздел *Тестирование* пока в разработке.")
    elif query.data == 'links':
        keyboard = [
            [InlineKeyboardButton("Вернуться к выбору раздела", callback_data='welcome')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Привет, дорогой друг! В этом сообщении собраны самые важные и нужные ссылки/документы:\n\n"
            "[Велкамбук](https://drive.google.com/file/d/1lKWZaLSD_6R53uFRUVMn0q3hKIvdeUs2/view?usp=drivesdk) - наша библия с особенностями заведения. Тут ты узнаешь про все особенности нашего заведения, какие люди стоят за \"Хачапури и Вино\", наши идеи и ценности, рекорды и достижения.\n\n"
            "[Методичка по кухне](https://docs.google.com/spreadsheets/d/1IyBrg_YnaDzy7VZcPp2KCfwuEiFir1ByQysadEraq0I/edit) - тут есть все составы блюд, которые помогут тебе при сдаче меню.\n\n"
            "[Канал новостей Пятницкой](https://t.me/+lv9AiwrkQqg3ZDEy) - обязательно для вступления, уведомления не выключай! Тут пишут все важные новости нашей точки, даты собраний, генеральных уборок и всё-всё-всё.\n\n"
            "[Канал новостей всех ХиВов Москвы](https://t.me/+3kLsRujJ0TljYzcy) - обязательно для вступления, уведомления не выключай! Тут пишут про все ближайшие события, тренинги, собеседования и внерабочие мероприятия.\n\n"
            "[Винная карта](https://docs.google.com/spreadsheets/d/1fj4u2RV8C_o2dBZlVK6GMTFMuE0o1tWhvC4FhgWZftU/edit) - здесь подробно рассказано про наши алкогольные и безалкогольные напитки, характеристика вин, интересные слова и базовые термины.\n\n"
            "[Органика и биодинамика](https://docs.google.com/document/d/1ictkvYCBSmUzi22oUDDWh-2yYdLjNLrGjqEfYk5U7ZA/edit) - подробно о концепциях органических и биодинамических напитков.\n\n"
            "[Чек-лист открытия и закрытия](https://docs.google.com/document/d/1ln1Rd3a-8-JFcgLLmmo9bzybnaz3YiLdhSCoLysM1hw/edit) - поможет тебе проверить себя при открытии и закрытии, делай все по этому документу, и хорошая смена тебе и коллегам обеспечена.\n\n"
            "[Методичка от Насти](https://docs.google.com/spreadsheets/d/10u-ZkZt7nCjLPixNlWTZwo95U0hdXxxE0OvbLFTUoFc/edit) - здесь собраны личные заметки по всем напиткам и информация с тренингов, которая поможет тебе при сдаче винки.\n\n"
            "[Глоссарий от Насти по алкоголю](https://docs.google.com/document/d/1147IG9YihAOw3NxWf9HbMUrOoH3nnXrqmnlC5vuyO_g/edit) - сборник всех возможных терминов из всех методичек по алкогольным напиткам.\n\n"
            "[Глоссарий грузинских блюд от Славы](https://docs.google.com/document/d/1mdbpluCw5NW0TsMrrXNY0Y_FbOZumGeipy8hnNe0xyU/edit) - если тебе интересно происхождение грузинских названий в нашем меню, прочитай этот файлик. Он будет полезен для ответов на вопросы гостей, например: \"почему вы не готовите горячий сациви?\" и \"почему оджахури и аджарули это не одно и то же?\".\n\n"
            "[Гайд по работе с iiko waiter](https://drive.google.com/file/d/1HTukWGYRy-TOCq3StPpH4OgfaOQ3iIcG/view?usp=drivesdk) - если ты уже научился хорошо пользоваться iiko, самое время научиться пользоваться waiter для оптимизации своей работы.\n\n"
            "[Полезная заметка на тему \"Традиции грузинского застолья. Супра\"](https://drive.google.com/file/d/1wYFnLiXfFrqvT6n3DJP6N6gyZz2jKsVi/view?usp=drivesdk) от Димы.\n\n"
            "[Полезная заметка на тему \"English for HIV\"](https://drive.google.com/file/d/1zO79LBn0vK3z8i_SQPb6EusQNa1WSmLE/view?usp=drivesdk) от Полины.\n\n"
            "[Полезная заметка на тему \"Сорта винограда\"](https://drive.google.com/file/d/1D5zoCeApaJImyNJqUnwiCW0MO_wOc-Yy/view?usp=drivesdk) от Деш.\n\n"
            "[Чек-лист работы с доставками](https://drive.google.com/file/d/1RR0L56LFRY55SxZfv1LnLgPr-0aGFzpf/view?usp=drivesdk) - здесь собраны важные аспекты по сборке доставки. Прочитав этот документ, ты узнаешь много нового, даже если чувствуешь себя в этом уверенно.\n\n"
            "[Памятка сборщика доставок](https://t.me/+CQJNAWwZGsJiYjI6) - дополнительная информация для сборщиков доставок.\n\n"
            "[Канал \"Новое доставка\"](https://t.me/+U7PMXi6jJPZ41DKX).\n\n"
            "[Канал \"Справочник сборщика\"](https://t.me/+CQJNAWwZGsJiYjI6).\n\n"
            "[Скидки](spreadsheets/d/1s-3Sh9U1roUMVEVQ_UEBworPZ3fBpc8JxTReZDJT6j4/edit) - ознакомительная информация по скидкам (не совсем актуальная).\n\n"
            "[Ачивки](https://docs.google.com/spreadsheets/d/1_ZVlJ_m_4YjmPOkl8Rp-2eR-nv_tKIwhFdIEfvNL2YE/edit) - здесь ты можешь посмотреть, какие ачивки тебе нужно выполнить, чтобы стать официантом ПРО и СУПЕР.\n\n"
            "Эти материалы помогут тебе в работе и ответят на многие вопросы!",
            disable_web_page_preview=True,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(welcome, pattern='welcome'))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

