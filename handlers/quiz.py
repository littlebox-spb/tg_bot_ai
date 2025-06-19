"""Модуль для режима викторины"""

import services.gpt as gpt
from services.logger import logger

TOPIC = ["Физика", "Искусство", "ИТ", "Литература"]
INDEX_SHIFT = 41
answerList = None
success = 0
fail = 0


def initQuiz():
    """
    Reset all variables for the quiz mode.

    This function is useful for manually restarting the quiz mode.

    Returns:
        None
    """
    global success, fail, answerList
    success = 0
    fail = 0
    answerList = None


def startQuiz(mode):
    """
    Starts the quiz mode.

    This function sends a request to the GPT service to generate a question with 4 answers on the topic specified by the mode parameter.

    Args:
        mode (int): The topic of the question. Must be in the range from 41 to 44.

    Returns:
        str: The question with 4 answers from the GPT service, or an error message if the request fails.

    Raises:
        Exception: If the request to the GPT service fails.
    """

    global answerList
    if not answerList:
        logger.info("Викторина GPT успешно запущена")
        request = [
            {
                "role": "system",
                "content": f"Ты опытный создатель интересных викторин. \
                                Ты должен задать вопрос по теме {TOPIC[mode - INDEX_SHIFT]}, и предложить 4 варианта ответов на него, \
                                из которых правильный только один. Вопросы должны относится к РАЗНЫМ аспектам. Правильный ответ НЕ ПОКАЗЫВАТЬ!\
                                Варианты ответов должны быть расположены после вопроса в виде нумерованного списка.",
            },
            {
                "role": "user",
                "content": f"Задай мне вопрос по теме {TOPIC[mode - INDEX_SHIFT]}.",
            },
        ]
        logger.info(
            f"Запрос успешно сформирован. Тема викторины: {TOPIC[mode - INDEX_SHIFT]}"
        )
        try:
            response = gpt.ask_gpt(request)
            logger.info("Вопрос викторины успешно получен")
            answerList = [a for a in response.split("\n") if len(a) > 4]
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении вопроса от OpenAI: {e}")
            return "😕К сожалению, не удалось получить вопрос в данный момент. Попробуйте позже!"


def quizAnswer(mode, answer):
    """
    Checks the answer of the user to the question of the GPT service, or an error message if the request fails.

    Args:
        mode (int): The mode of the quiz.
        answer (int): The answer of the user.

    Returns:
        str: The response from the GPT service, or an error message if the request fails.

    Raises:
        Exception: If the request to the GPT service fails.
    """
    global answerList, success, fail
    if answerList:
        print(answerList, answer)
        question = answerList[0]
        answerList = [a[2:].strip() for a in answerList[1:]]
        request = [
            {
                "role": "system",
                "content": f"Ты задал вопрос {question} по теме {TOPIC[mode - INDEX_SHIFT]}. \
                Теперь ты должен ответить проверить ответ пользователя и написать правильно он ответил или нет. \
                Первое слово в ответе ДОЛЖНО быть 'Правильно' или 'Неправильно'.",
            },
            {
                "role": "user",
                "content": f"Правильный ответ на вопрос по теме {TOPIC[mode - INDEX_SHIFT]} - {answerList[int(answer) - 1]}.",
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
