import services.gpt as gpt
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def fact():
    with open("prompt/random.system.txt", "r", encoding="utf-8") as f:
        prompt_system = f.read()
        logger.info("System промпт успешно загружен")
    with open("prompt/random.user.txt", "r", encoding="utf-8") as f:
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
