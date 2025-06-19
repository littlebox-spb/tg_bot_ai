"""Главный модуль бота"""

import mode
from config import TG_BOT_KEY
from handlers.ask import ask
from handlers.quiz import initQuiz, quizAnswer, startQuiz
from handlers.random import fact
from handlers.star import dialog, startDialog
from handlers.translate import translate
from handlers.trenager import getWorld, newTrain, question, testWords
from services.logger import logger
from telebot import TeleBot, types

bot = TeleBot(TG_BOT_KEY)
Mode = mode.MAIN_MENU


def main_menu():
    """
    Generate main menu markup.

    Returns:
        markup (types.ReplyKeyboardMarkup): Reply markup with main menu buttons.
    """
    global Mode
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌍 Факт")
    btn2 = types.KeyboardButton("❓ чату GPT")
    btn3 = types.KeyboardButton("✨ Звезда")
    btn4 = types.KeyboardButton("🎯 Викторина")
    btn5 = types.KeyboardButton("📖 Переводчик")
    btn6 = types.KeyboardButton("📑 Тренажёр")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    Mode = 0
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    """
    Handles the /start command.

    Sends a greeting message to the user with main menu markup.
    """
    bot.send_message(
        message.chat.id,
        text="Привет! Я бот и я могу развлечь тебя. Выбери, что ты хочешь.",
        reply_markup=main_menu(),
    )
    logger.info("Бот запущен")


@bot.message_handler(content_types=["text"])
def actions(message):
    """
    Handles text messages from users.

    If the message is a command, it calls the corresponding function.
    If the message is a text, it sends the text to the corresponding mode
    (e.g. random fact, quiz, dialog with celebrity, etc.).
    """
    global Mode
    if message.text == "🌍 Факт":
        logger.info("Случайный факт успешно запущен")
        if Mode != mode.RANDOM:
            bot.send_message(
                message.chat.id,
                text="Хорошо, я сейчас подыщу тебе, что-нибудь интересное!",
            )
            with open("picturies/random.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.RANDOM
    elif message.text == "❓ чату GPT":
        logger.info("Режим работы с GPT успешно запущен")
        with open("picturies/gpt.jpg", "rb") as img:
            bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.QUESTIONS
        message.text = "Можно задать тебе вопрос?"
    elif message.text == "✨ Звезда":
        logger.info("Разговор со звездой успешно запущен")
        if Mode != mode.DIALOG:
            with open("picturies/zvezda.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.DIALOG
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
        if Mode != mode.QUIZ:
            with open("picturies/quiz.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.QUIZ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Физика")
        btn2 = types.KeyboardButton("Искусство")
        btn3 = types.KeyboardButton("ИТ")
        btn4 = types.KeyboardButton("Литература")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(
            message.chat.id, text="Выбери тему викторины", reply_markup=markup
        )
    elif message.text == "📖 Переводчик":
        logger.info("Перевочик успешно запущен")
        if Mode != mode.TRANSLATE:
            with open("picturies/translate.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.TRANSLATE
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
    elif message.text == "📑 Тренажёр":
        logger.info("Словарный тренажёр успешно запущен")
        if Mode != mode.TRAIN:
            with open("picturies/trenager.jpg", "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img)
        Mode = mode.TRAIN
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
    if Mode in (mode.ENGLISH, mode.FRENCH, mode.CHINESE, mode.ARABIC):
        bot.send_message(message.chat.id, text=translate(Mode, message.text))
    elif Mode in (mode.DJONNY, mode.DJENIFER, mode.ROBERT, mode.HLOYA):
        bot.send_message(message.chat.id, text=dialog(Mode, message.text))
    elif Mode == mode.TRENAGER:
        bot.send_message(message.chat.id, text=testWords(message.text))
    match Mode:
        case mode.RANDOM:
            bot.send_message(
                message.chat.id,
                text="Я ищу интересный факт...",
            )
            bot.send_message(message.chat.id, text=fact())
        case mode.QUESTIONS:
            bot.send_message(message.chat.id, text=ask(message.text))
        case mode.DIALOG:
            match message.text:
                case "Джонни Депп":
                    logger.info("Выбран Джонни Депп")
                    Mode = mode.DJONNY
                    with open("picturies/Johnny_Depp.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Дженифер Лоуренс":
                    logger.info("Выбрана Дженифер Лоуренс")
                    Mode = mode.DJENIFER
                    with open("picturies/Jennifer_Lawrence.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Роберт Дауни мл.":
                    logger.info("Выбран Роберт Дауни мл.")
                    Mode = mode.ROBERT
                    with open("picturies/Robert_Downey_Jr.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Хлоя Грейс Морец":
                    logger.info("Выбрана Хлоя Грейс Морец")
                    Mode = mode.HLOYA
                    with open("picturies/Chloë_Grace_Moretz.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
            if Mode in (mode.DJONNY, mode.DJENIFER, mode.ROBERT, mode.HLOYA):
                bot.send_message(
                    message.chat.id,
                    text="Для смены персонажа нажми 'Главное меню'.",
                )
                bot.send_message(message.chat.id, startDialog(Mode))
        case mode.QUIZ | mode.PHISICS | mode.ART | mode.IT | mode.LITERATURE:
            match message.text:
                case "Физика":
                    logger.info("Выбран тема Физика")
                    Mode = mode.PHISICS
                    with open("picturies/fizika.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Искусство":
                    logger.info("Выбрана тема Искусство")
                    Mode = mode.ART
                    with open("picturies/iskusstvo.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "ИТ":
                    logger.info("Выбран тема ИТ.")
                    Mode = mode.IT
                    with open("picturies/it.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
                case "Литература":
                    logger.info("Выбрана тема Литература")
                    Mode = mode.LITERATURE
                    with open("picturies/literature.jpg", "rb") as img:
                        bot.send_photo(chat_id=message.chat.id, photo=img)
            if Mode in (mode.PHISICS, mode.ART, mode.IT, mode.LITERATURE):
                bot.send_message(
                    message.chat.id,
                    text="Для смены темы викторины нажми 'Главное меню'.",
                )
                bot.send_message(message.chat.id, quizAnswer(Mode, message.text))
                bot.send_message(message.chat.id, text="Готовлю вопрос к викторине...")
                bot.send_message(message.chat.id, startQuiz(Mode))
            else:
                initQuiz()
        case mode.TRANSLATE:
            match message.text:
                case "Английский":
                    logger.info("Выбран английский язык")
                    Mode = mode.ENGLISH
                case "Французский":
                    logger.info("Выбран французский язык")
                    Mode = mode.FRENCH
                case "Китайский":
                    logger.info("Выбран китайский язык")
                    Mode = mode.CHINESE
                case "Арабский":
                    logger.info("Выбран арабский язык")
                    Mode = mode.ARABIC
            if Mode in (mode.ENGLISH, mode.FRENCH, mode.CHINESE, mode.ARABIC):
                bot.send_message(
                    message.chat.id,
                    text="Введи текст, который нужно перевести. Для смены языка нажми 'Главное меню'.",
                )
        case mode.TRAIN | mode.WORLD | mode.TRENAGER:
            match message.text:
                case "Ещё слово":
                    logger.info("Запрошено ещё слово")
                    Mode = mode.WORLD
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
                        Mode = mode.TRENAGER
                    except StopIteration:
                        Mode = mode.WORLD
                        newTrain()
        case mode.MAIN_MENU:
            bot.send_message(message.chat.id, text="Выбери, что ты хочешь.")
            initQuiz()


def main():
    """
    The main function to start the Telegram bot.

    This function initializes and starts the bot's infinite polling loop,
    listening for incoming messages and handling them accordingly. If an
    exception occurs during polling, it logs the error message.
    """

    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
