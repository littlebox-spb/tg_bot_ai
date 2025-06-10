import logging

import services.gpt as gpt

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def translate(Mode, message):
    logger.info("Переводчик GPT успешно запущен")
    language = ["английский", "французский", "китайский", "арабский"]
    request = [
        {"role": "system", "content": "Ты переводчик - полиглот."},
        {
            "role": "user",
            "content": f'Переведи "{message.text}" на {language[Mode - 51]} язык.',
        },
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Перевод успешно получен")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении перевода от OpenAI: {e}")
        return "😕К сожалению, не удалось получить перевод в данный момент. Попробуйте позже!"
