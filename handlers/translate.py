"""Модуль для режима переводов"""

import services.gpt as gpt
from services.logger import logger

INDEX_SHIFT = 51


def translate(Mode, message):
    """
    Translates a given message to a language specified by Mode.

    Args:
        Mode (int): The mode of the translation. Must be in the range from 51 to 54.
        message (str): The message to be translated.

    Returns:
        str: The translation of the message from the GPT service, or an error message if the request fails.

    Raises:
        Exception: If the request to the GPT service fails.
    """
    logger.info("Переводчик GPT успешно запущен")
    language = ["английский", "французский", "китайский", "арабский"]
    request = [
        {"role": "system", "content": "Ты переводчик - полиглот."},
        {
            "role": "user",
            "content": f'Переведи "{message}" на {language[Mode - INDEX_SHIFT]} язык.',
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
