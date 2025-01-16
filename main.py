from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')
language = "None"
button_reply = {"RU":"Вы выбрали русский язык","EN":"You've chosen english"}
text_reply = {"RU": "Текстовое сообщение получено!", "EN": "We’ve received a message from you!", "None": "Выберете язык интерфейса"}
voce_reply = {"RU": "Голосовое сообщение получено", "EN": "We’ve received a voice message from you!", "None": "Выберете язык интерфейса"}
image_reply = {"RU": "Фотография сохранена", "EN": "Photo saved!", "None": "Выберете язык интерфейса"}
# INLINE
# форма inline клавиатуры
inline_frame = [[InlineKeyboardButton("English", callback_data="EN")],
                [InlineKeyboardButton("Русский", callback_data="RU")]]
# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)

# функция-обработчик команды /start
async def start(update: Update, _):

    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text('Выберите язык интерфейса', reply_markup=inline_keyboard)


# функция-обработчик нажатий на кнопки
async def button(update: Update, _):
    # получаем callback query из update
    query = update.callback_query

    # всплывающее уведомление
    await query.answer('OK!')
    global language
    language = query.data
    # редактируем сообщение после нажатия
    await query.edit_message_text(text=button_reply[language])


# функция-обработчик команды /help
async def help(update, context):
    await update.message.reply_text("Этот под предназначен для обучения!\U00002757")


# функция-обработчик текстовых сообщений
async def text(update, context):

    await update.message.reply_text(text_reply[language])


# функция-обработчик сообщений с изображениями
async def image(update, context):
    await update.message.reply_text(image_reply[language])

    # получаем изображение из апдейта
    file = await update.message.photo[-1].get_file()

    # сохраняем изображение на диск
    await file.download_to_drive("./photos/image.jpg")


# функция-обработчик голосовых сообщений
async def voice(update, context):
    await update.message.reply_text(voce_reply[language])

def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с фотографиями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()