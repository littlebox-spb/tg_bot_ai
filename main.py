import logging

from config import TG_BOT_KEY
from handlers.ask import ask
from handlers.random import fact
from handlers.star import dialog, startDialog
from handlers.translate import translate
from handlers.trenager import getWorld, question, statistics, testWords
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
        with open("picturies/gpt.jpg", "rb") as img:
            bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = 2
    elif message.text == "✨ Поговорить со звездой":
        logger.info("Разговор со звездой успешно запущен")
        if Mode != 3:
            with open("picturies/zvezda.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = 3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Джонни Депп")
        btn2 = types.KeyboardButton("Дженифер Лоуренс")
        btn3 = types.KeyboardButton("Роберт Дауни мл.")
        btn4 = types.KeyboardButton("Хлоя Грейс Морец")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(
            message.chat.id, text="Выбери звезду для беседы", reply_markup=markup
        )
    elif message.text == "🎯 Викторина":
        logger.info("Викторина успешно запущена")
        Mode = 4
        bot.send_message(message.chat.id, text="Хорошо, давай начнем викторину!")
    elif message.text == "📖 Переводчик":
        logger.info("Перевочик успешно запущен")
        if Mode != 5:
            with open("picturies/translate.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
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
        if Mode != 6:
            with open("picturies/trenager.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = 6
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ещё слово")
        btn2 = types.KeyboardButton("Тренироваться")
        back = types.KeyboardButton("Закончить")
        markup.add(btn1, btn2, back)
        bot.send_message(
            message.chat.id,
            text="Я подыскиваю для тебя интересное слово...",
        )
        bot.send_message(
            message.chat.id,
            text=getWorld(),
            reply_markup=markup,
        )
    elif message.text == "Главное меню" or message.text == "Закончить":
        logger.info("Возврат в главное меню")
        bot.send_message(
            message.chat.id,
            text="Вы вернулись в главное меню",
            reply_markup=main_menu(),
        )
    if Mode in (
        51,
        52,
        53,
        54,
    ):  # 51 - Английский, 52 - Французский, 53 - Китайский, 54 - Арабский
        bot.send_message(message.chat.id, text=translate(Mode, message.text))
    elif (
        Mode in (31, 32, 33, 34)
    ):  # 31 - Джонни Депп, 32 - Дженифер Лоуренс, 33 - Роберт Дауни мл., 34 - Хлоя Грейс Морец
        bot.send_message(message.chat.id, text=dialog(Mode, message.text))
    elif Mode == 62:  # Тренироваться
        bot.send_message(message.chat.id, text=testWords(message.text))
    match Mode:
        case 1:  # Cлучайный факт
            bot.send_message(
                message.chat.id,
                text="Я ищу интересный факт...",
            )
            bot.send_message(message.chat.id, text=fact())
        case 2:  # Режим работы с GPT
            bot.send_message(message.chat.id, text=ask(message.text))
        case 3:  # Разговор со звездой
            match message.text:
                case "Джонни Депп":
                    logger.info("Выбран Джонни Депп")
                    Mode = 31
                    with open("picturies/Johnny Depp.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Дженифер Лоуренс":
                    logger.info("Выбрана Дженифер Лоуренс")
                    Mode = 32
                    with open("picturies/Jennifer Lawrence.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Роберт Дауни мл.":
                    logger.info("Выбран Роберт Дауни мл.")
                    Mode = 33
                    with open("picturies/Robert Downey Jr.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Хлоя Грейс Морец":
                    logger.info("Выбрана Хлоя Грейс Морец")
                    Mode = 34
                    with open("picturies/Chloë Grace Moretz.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
            if (
                Mode in (31, 32, 33, 34)
            ):  # 31 - Джонни Депп, 32 - Дженифер Лоуренс, 33 - Роберт Дауни мл., 34 - Хлоя Грейс Морец
                bot.send_message(
                    message.chat.id,
                    text="Для смены персонажа нажми 'Главное меню'.",
                )
                bot.send_message(message.chat.id, startDialog(Mode))
        case 4:  # Квиз
            bot.send_message(message.chat.id, text="quiz(message.text)")
        case 5:  # Перевод
            match message.text:
                case "Английский":
                    logger.info("Выбран английский язык")
                    Mode = 51
                case "Французский":
                    logger.info("Выбран французский язык")
                    Mode = 52
                case "Китайский":
                    logger.info("Выбран китайский язык")
                    Mode = 53
                case "Арабский":
                    logger.info("Выбран арабский язык")
                    Mode = 54
            if Mode in (
                51,
                52,
                53,
                54,
            ):  # 51 - Английский, 52 - Французский, 53 - Китайский, 54 - Арабский
                bot.send_message(
                    message.chat.id,
                    text="Введи текст, который нужно перевести. Для смены языка нажми 'Главное меню'.",
                )
        case 6 | 61 | 62:  # Словарный тренажёр
            match message.text:
                case "Ещё слово":
                    logger.info("Запрошено ещё слово")
                    Mode = 61
                    bot.send_message(
                        message.chat.id,
                        text="Я подыскиваю для тебя интересное слово...",
                    )
                    bot.send_message(message.chat.id, text=getWorld())
                case "Тренироваться":
                    logger.info("Выбран режим тренировки")
                    bot.send_message(
                        message.chat.id,
                        text="Для тренировки нажимай 'Тренироваться'.",
                    )
                    try:
                        bot.send_message(message.chat.id, text=question())
                        Mode = 62
                    except StopIteration:
                        bot.send_message(
                            message.chat.id,
                            text="Тренировка закончилась. " + statistics(),
                        )
        case 0:  # Главное меню
            bot.send_message(message.chat.id, text="Выбери, что ты хочешь.")


def main():
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
