import services.gpt as gpt
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def ask(prompt):
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
