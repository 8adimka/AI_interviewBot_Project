import os
import openai
from bot.services.dto.gpt_request import GptRequest, Message
from bot.services.dto.gpt_response import GptResponse
from bot.config import Config

class GptClient:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("Переменная окружения OPENAI_API_KEY не установлена.")
        openai.api_key = self.api_key

    def get_gpt_response(self, prompt: str) -> str:
        """
        Отправляет запрос в OpenAI API и возвращает ответ.
        """
        messages = [
            Message(role="system", content=Config.OPENAI_SYSTEM_ROLE),
            Message(role="user", content=prompt)
        ]
        request = GptRequest(model=Config.OPENAI_CHAT_MODEL, messages=messages)

        try:
            response = openai.ChatCompletion.create(
                model=request.model,
                messages=[msg.__dict__ for msg in request.messages]
            )
            gpt_response = GptResponse(**response)
            return gpt_response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            raise Exception(f"Ошибка при запросе к OpenAI API: {e}")
