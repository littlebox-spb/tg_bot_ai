"""Модуль для режима диалогов с звездами"""

import services.gpt as gpt
from services.logger import logger

STARS = ["Джонни Депп", "Дженифер Лоуренс", "Роберт Дауни мл.", "Хлоя Грейс Морец"]
INDEX_SHIFT = 31


def startDialog(mode):
    """
    Initiates a dialog as a celebrity.

    This function sends a request to the GPT service to start a conversation as a selected celebrity
    based on the provided mode.

    Args:
        mode (int): The index of the celebrity in the STARS list. It should match the respective
                    celebrity's index adjusted by INDEX_SHIFT.

    Returns:
        str: The initial response from the GPT service as the celebrity, or an error message if the
             request fails.
    """

    request = [
        {
            "role": "system",
            "content": f"Ты {STARS[mode - INDEX_SHIFT]}! Перед тобой очень интересный человека и ты хочешь с ним поговорить.",
        },
        {"role": "user", "content": f"Начни разговор как {STARS[mode - INDEX_SHIFT]}."},
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Ответ успешно получен")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении факта от OpenAI: {e}")
        return "😕К сожалению, не удалось начать беседу в данный момент. Попробуйте зайти позже!"


def dialog(mode, prompt):
    """
    Continues a dialog as a celebrity.

    This function sends a request to the GPT service to continue a conversation as a selected celebrity
    based on the provided mode.

    Args:
        mode (int): The index of the celebrity in the STARS list. It should match the respective
                    celebrity's index adjusted by INDEX_SHIFT.
        prompt (str): The message to send to the GPT service to continue the dialog.

    Returns:
        str: The response from the GPT service as the celebrity, or an error message if the
             request fails.
    """

    request = [
        {
            "role": "system",
            "content": f"Ты {STARS[mode - 31]}! Продолжи беседу, как {STARS[mode - INDEX_SHIFT]}!",
        },
        {"role": "user", "content": prompt},
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Ответ успешно получен")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
        return "😕К сожалению, не удалось получить ответ в данный момент. Попробуйте задать ваш вопрос позже!"
