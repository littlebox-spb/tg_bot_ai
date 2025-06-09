import logging

from config import TG_BOT_KEY
from handlers.random import fact
from telebot import TeleBot, types

bot = TeleBot(TG_BOT_KEY)
Mode = 0  # Режим главного меню

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main_menu():
    global Mode
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌍 Случайный факт")
    btn2 = types.KeyboardButton("❓ Задать вопрос чату GPT")
    btn3 = types.KeyboardButton("✨ Поговорить со звездой")
    btn4 = types.KeyboardButton("🎯 Викторина")
    btn5 = types.KeyboardButton("📖 Переводчик")
    btn6 = types.KeyboardButton("📑 Словарный тренажёр английского языка")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    Mode = 0
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        text="Привет! Я бот и я могу развлечь тебя. Выбери, что ты хочешь.",
        reply_markup=main_menu(),
    )
    logger.info("Бот запущен")


@bot.message_handler(content_types=["text"])
def actions(message):
    global Mode
    if message.text == "🌍 Случайный факт":
        logger.info("Случайный факт успешно запущен")
        if Mode != 1:
            bot.send_message(
                message.chat.id,
                text="Хорошо, я сейчас подыщу тебе, что-нибудь интересное!",
            )
            with open("picturies/random.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = 1
    elif message.text == "❓ Задать вопрос чату GPT":
        logger.info("Режим работы с GPT успешно запущен")
        Mode = 2
        bot.send_message(message.chat.id, text="Я тебя слушаю, спрашивай!")
    elif message.text == "✨ Поговорить со звездой":
        logger.info("Разговор со звездой успешно запущен")
        Mode = 3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Джонни Депп")
        btn2 = types.KeyboardButton("Дженифер Лоуренс")
        btn3 = types.KeyboardButton("Роберт Дауни мл.")
        btn4 = types.KeyboardButton("Хлоя Грейс Морец")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Выбери персонажа", reply_markup=markup)
    elif message.text == "🎯 Викторина":
        logger.info("Викторина успешно запущена")
        Mode = 4
        bot.send_message(message.chat.id, text="Хорошо, давай начнем викторину!")
    elif message.text == "📖 Переводчик":
        logger.info("Перевочик успешно запущен")
        Mode = 5
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Английский")
        btn2 = types.KeyboardButton("Французский")
        btn3 = types.KeyboardButton("Китайский")
        btn4 = types.KeyboardButton("Арабский")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(
            message.chat.id,
            text="Выбери язык, на который нужно перевести твое сообщение.",
            reply_markup=markup,
        )
    elif message.text == "📑 Словарный тренажёр английского языка":
        logger.info("Словарный тренажёр успешно запущен")
        Mode = 6
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ещё слово")
        btn2 = types.KeyboardButton("Тренироваться")
        back = types.KeyboardButton("Закончить")
        markup.add(btn1, btn2, back)
        bot.send_message(
            message.chat.id,
            text="Тут должно быть слово, которое нужно перевести.",
            reply_markup=markup,
        )
    elif message.text == "Главное меню" or message.text == "Закончить":
        logger.info("Возврат в главное меню")
        bot.send_message(
            message.chat.id,
            text="Вы вернулись в главное меню",
            reply_markup=main_menu(),
        )
    match Mode:
        case 1:
            bot.send_message(message.chat.id, text=fact())
        case 2:
            bot.send_message(message.chat.id, text=f"ask({message.text})")
        case 3:
            bot.send_message(message.chat.id, text=f"dialog({message.text})")
        case 4:
            bot.send_message(message.chat.id, text="quiz(message.text)")
        case 5:
            bot.send_message(message.chat.id, text="translate(message.text)")
        case 6:
            bot.send_message(message.chat.id, text="learn(message.text)")
        case 0:
            bot.send_message(message.chat.id, text="Выбери, что ты хочешь.")


def main():
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
