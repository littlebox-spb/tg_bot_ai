from config import GPT_API_KEY
from openai import OpenAI

client = OpenAI(api_key=GPT_API_KEY)


def ask_gpt(request):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[request],
        max_tokens=200,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()
