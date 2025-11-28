# utils/ai_bot.py

from openai import OpenAI
from django.conf import settings
import os


client = OpenAI(

    base_url="https://openrouter.ai/api/v1",
    api_key=settings.GEMINI_API_KEY,
)


def get_ai_response(prompt, history):
    """
    Отправляет промпт и историю сообщений в DeepSeek API.
    History - список объектов вида [{'role': 'user', 'content': '...'}]
    """

    system_message = {
        "role": "system",
        "content": "Ты — умный AI-ассистент, встроенный в платформу онлайн-обучения LMS. "
            "Твоя главная задача: помогать пользователю **ориентироваться в контенте сайта** "
            "и **выбирать, чем заняться дальше** (например, какой курс изучить, какой тест пройти, "
            "или что повторить). "
            "Всегда отвечаешь дружелюбно, полезно и **строго на русском языке**. "
            "Избегай общих фраз и фокусируйся на **обучении и функционале сайта**."    }

    messages = [system_message]
    # Добавляем историю разговора, чтобы бот помнил контекст
    messages.extend(history)

    # Добавление текущего сообщения пользователя
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="tngtech/tng-r1t-chimera:free",
            messages=messages,
        )
        return response.choices[0].message.content

    except Exception as e:
        # !!! ИСПРАВЛЕННЫЙ БЛОК: Выводим полный текст ошибки !!!
        print("--------------------------------------------------")
        print(f"КРИТИЧЕСКАЯ ОШИБКА Gemini API: {type(e).__name__}")
        print(f"Полный текст ошибки: {e}")
        print("--------------------------------------------------")
        # !!! ---------------------------------------------------- !!!
        return "Извините, произошла ошибка связи с AI."