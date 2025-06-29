import os

from dotenv import load_dotenv

load_dotenv()

GPT_API_KEY = os.getenv("GPT_API_KEY")
TG_BOT_KEY = os.getenv("TG_BOT_KEY")
PROXY_URL = os.getenv("PROXY_URL")

if not all([GPT_API_KEY, TG_BOT_KEY]):
    raise Exception("Не заполнены переменные окружения.")
