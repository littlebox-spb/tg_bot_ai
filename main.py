import logging

from config import TG_BOT_KEY
from telebot import TeleBot
from telebot.types import Message

bot = TeleBot(TG_BOT_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@bot.message_handler(commands=["random"])
def start_cmd(message: Message):
    pass


@bot.message_handler(commands=["gpt"])
def help_cmd(message: Message):
    pass


@bot.message_handler(commands=["talk"])
def help_cmd(message: Message):
    pass


@bot.message_handler(commands=["quiz"])
def help_cmd(message: Message):
    pass


def main():
    try:
        bot.infinity_polling()
        logger.info("Бот запущен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
