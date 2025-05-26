import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TG_BOT_KEY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        application = Application.builder().token(TG_BOT_KEY).build()
        application.add_handler(CommandHandler("start", start)) 
        application.add_handler(CommandHandler("random", start)) 


        logger.info("Бот запущен")
        application.run_polling()

    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()