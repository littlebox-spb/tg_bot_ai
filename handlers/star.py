import services.gpt as gpt
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
STARS = ["Джонни Депп", "Дженифер Лоуренс", "Роберт Дауни мл.", "Хлоя Грейс Морец"]


def startDialog(mode):
    request = [
        {
            "role": "system",
            "content": f"Ты {STARS[mode - 31]}! Перед тобой очень интересный человека и ты хочешь с ним поговорить.",
        },
        {"role": "user", "content": f"Начни разговор как {STARS[mode - 31]}."},
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
    request = [
        {
            "role": "system",
            "content": f"Ты {STARS[mode - 31]}! Продолжи беседу, как {STARS[mode - 31]}!",
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
