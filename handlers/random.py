"""Модуль для режима случайных фактов"""

import services.gpt as gpt
from services.logger import logger


def fact():
    """
    Gets a random fact from the GPT service.

    Returns:
        str: The response from the GPT service, or an error message if the request fails.
    """
    with open("prompt/random_system.txt", "r", encoding="utf-8") as f:
        prompt_system = f.read()
        logger.info("System промпт успешно загружен")
    with open("prompt/random_user.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
        logger.info("Промпт успешно загружен")
    request = [
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": prompt},
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Факт успешно получен")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении факта от OpenAI: {e}")
        return (
            "😕К сожалению, не удалось получить факт в данный момент. Попробуйте позже!"
        )
