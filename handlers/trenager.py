import services.gpt as gpt
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
words = []
gen = None
testWord = ""
success = 0


def getWorld():
    request = [
        {
            "role": "system",
            "content": f"Ты учитель английского языка. Твоя задача дать ученику слово с примерами его использования. \
                Напиши слово на английском языке, а после перевод слова и примеры его использования. Слова не должны быть из списка {words}. \
                Не используй никого обрамления слова символами.",
        },
        {
            "role": "user",
            "content": "Дай мне слово для заучивания с переводом и примерами.",
        },
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        words.append(response[:50].split()[0])
        logger.info(f"Ответ успешно получен, слово {words[-1]} добавлено в список")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении слова от OpenAI: {e}")
        return "😕К сожалению, не удалось получить слово в данный момент. Попробуйте зайти позже!"


def statistics():
    return f"Вы успешно ответили на {success} вопросов из {len(words)}."


def wordsGeneration():
    for word in words:
        yield word


def question():
    global gen, success, testWord
    if gen is None:
        gen = wordsGeneration()
        success = 0
    testWord = next(gen)
    return f"Как переводится слово {testWord}?"


def testWords(prompt):
    global success
    request = [
        {
            "role": "system",
            "content": "Ты учитель английского языка. Твоя задача проверить знания ученика. Отвечай только да или нет.",
        },
        {
            "role": "user",
            "content": f"Скажи, правильно ли переводится слово {testWord} на английский язык - {prompt}.",
        },
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Ответ успешно получен")
        if "да" in response.lower():
            success += 1
        return question()
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
        return "😕К сожалению, не удалось получить ответ в данный момент. Попробуйте задать ваш вопрос позже!"
