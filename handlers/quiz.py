import services.gpt as gpt
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
TOPIC = ["Физика", "Искусство", "ИТ", "Литература"]
answerList = None
success = 0
fail = 0


def initQuiz():
    global success, fail, answerList
    success = 0
    fail = 0
    answerList = None


def startQuiz(mode):
    global answerList
    if not answerList:
        logger.info("Викторина GPT успешно запущена")
        request = [
            {
                "role": "system",
                "content": f"Ты опытный создатель интересных викторин. \
                                Ты должен задать вопрос по теме {TOPIC[mode - 41]}, и предложить 4 варианта ответов на него, \
                                из которых правильный только один. Вопросы должны относится к РАЗНЫМ аспектам. Правильный ответ НЕ ПОКАЗЫВАТЬ!\
                                Варианты ответов должны быть расположены после вопроса в виде нумерованного списка.",
            },
            {
                "role": "user",
                "content": f"Задай мне вопрос по теме {TOPIC[mode - 41]}.",
            },
        ]
        logger.info(f"Запрос успешно сформирован. Тема викторины: {TOPIC[mode - 41]}")
        try:
            response = gpt.ask_gpt(request)
            logger.info("Вопрос викторины успешно получен")
            answerList = [a for a in response.split("\n") if len(a) > 4]
            answerList = [a[2:].strip() for a in answerList[1:]]
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении вопроса от OpenAI: {e}")
            return "😕К сожалению, не удалось получить вопрос в данный момент. Попробуйте позже!"


def quizAnswer(mode, answer):
    global answerList, success, fail
    if answerList:
        request = [
            {
                "role": "system",
                "content": f"Ты задал вопрос {answerList[0]} по теме {TOPIC[mode - 41]}. \
                Теперь ты должен ответить проверить ответ пользователя и написать правильно он ответил или нет. \
                Первое слово в ответе ДОЛЖНО быть 'Правильно' или 'Неправильно'.",
            },
            {
                "role": "user",
                "content": f"Правильный ответ на вопрос по теме {TOPIC[mode - 41]} - {answerList[int(answer)]}.",
            },
        ]
        logger.info("Ответ успешно сформирован")
        try:
            response = gpt.ask_gpt(request)
            logger.info("Ответ викторины успешно получен")
            if response == "Правильно.":
                success += 1
            else:
                fail += 1
            return (
                response
                + f"\nПравильных ответов: {success}\nНеправильных ответов: {fail}"
            )
        except Exception as e:
            logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
            return "😕К сожалению, не удалось получить ответ в данный момент. Попробуйте позже!"
        finally:
            answerList = None
    else:
        return "Введите номер правильного ответа."
