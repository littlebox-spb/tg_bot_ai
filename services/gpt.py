import httpx as httpx
from config import GPT_API_KEY
from openai import OpenAI

client = OpenAI(
    http_client=httpx.Client(proxy="http://18.199.183.77:49232"), api_key=GPT_API_KEY
)


def ask_gpt(request):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=request,
        max_tokens=3000,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()
