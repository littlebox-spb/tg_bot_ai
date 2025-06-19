"""Модуль для режима тренировки слов английского языка"""

import services.gpt as gpt
from services.logger import logger

words = []
gen = None
testWord = ""
success = 0


def getWorld():
    """
    Retrieves a new English word for the user to learn along with its translation and usage examples.

    This function sends a request to the GPT service to obtain a word that is not already in the `words` list.
    The response includes the word in English, its translation, and examples of its usage. The word is then
    appended to the `words` list to prevent repetition in future requests.

    Returns:
        str: The response from the GPT service containing the word, its translation, and examples, or an
             error message if the request fails.
    """

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


def newTrain():
    """
    Resets the training process by clearing the list of words and resetting the word generation generator and the success counter.
    """
    global gen, words, success
    gen = None
    words = []
    success = 0


def wordsGeneration():
    """
    Generates a sequence of words that the user has seen so far.

    Yields:
        str: The next word in the sequence.
    """
    for word in words:
        yield word


def question():
    """
    Asks the user a question about the translation of the next word in the sequence of words seen so far.

    If the sequence has not been started yet, it is initialized with the list of words seen so far. The success counter is also reset to 0.

    Returns:
        str: The next word in the sequence along with a question asking for its translation.
    """
    global gen, success, testWord
    if gen is None:
        gen = wordsGeneration()
        success = 0
    testWord = next(gen)
    return f"Как переводится слово {testWord}?"


def testWords(prompt):
    """
    Checks the answer of the user to the translation of the next word in the sequence of words seen so far.

    Args:
        prompt (str): The user's answer to the translation of the next word in the sequence of words seen so far.

    Returns:
        str: The next word in the sequence along with a question asking for its translation, or the result of the training.
    """
    global success
    request = [
        {
            "role": "system",
            "content": "Ты учитель английского языка. Твоя задача проверить знания ученика. Отвечай только да или нет.",
        },
        {
            "role": "user",
            "content": f"Скажи, правильно ли переводится слово {testWord} на русский язык - {prompt}.",
        },
    ]
    logger.info("Запрос успешно сформирован")
    try:
        response = gpt.ask_gpt(request)
        logger.info("Ответ успешно получен")
        if "да" in response.lower():
            success += 1
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
        return "😕К сожалению, не удалось получить ответ в данный момент. Попробуйте задать ваш вопрос позже!"
    try:
        return question()
    except Exception as e:
        logger.error(f"Список слов пуст. {e}")
        return f"Тренировка закончилась. Вы успешно ответили на {success} вопросов из {len(words)}."
