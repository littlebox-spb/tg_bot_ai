"""Модуль для режима вопросов чату GPT"""

import services.gpt as gpt
from services.logger import logger


def ask(prompt):
    """
    Sends a question to the GPT service and returns the response.

    Args:
        prompt (str): The user's question to be sent to the GPT service.

    Returns:
        str: The response from the GPT service, or an error message if the request fails.
    """

    request = [
        {
            "role": "system",
            "content": "Ты знаток всего, который с удовольствием отвечает на вопросы.",
        },
        {"role": "user", "content": prompt},
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Ответ успешно получен")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении факта от OpenAI: {e}")
        return "😕К сожалению, не удалось получить ответ в данный момент. Попробуйте задать ваш вопрос позже!"
