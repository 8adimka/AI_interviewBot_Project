import requests
from dataclasses import asdict
from typing import Optional
import logging
from bot.config import Config
from bot.services.dto.gpt_request import GptRequest, Message
from bot.services.dto.gpt_response import GptResponse
from bot.models.models import Prompt, Question  # Импортируем модели Prompt и Question
from sqlalchemy.orm import Session
from sqlalchemy import func
from bot.database import SessionLocal

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAiClient:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("Переменная окружения OPENAI_API_KEY не установлена.")

        self.chat_api_url = Config.OPENAI_CHAT_URL
        self.chat_model = Config.OPENAI_CHAT_MODEL
        self.system_role = Config.OPENAI_SYSTEM_ROLE
        self.transcription_api_url = Config.OPENAI_TRANSCRIPTION_URL
        self.voice_model = Config.OPENAI_TRANSCRIPTION_MODEL
        self.language = Config.OPENAI_TRANSCRIPTION_LANGUAGE

    def get_random_question_from_db(self) -> Optional[Question]:
        """
        Возвращает случайный вопрос из базы данных.
        """
        db: Session = SessionLocal()
        try:
            # Используем ORDER BY RANDOM() для SQLite или аналогичные функции для других СУБД
            question = db.query(Question).order_by(func.random()).first()
            if not question:
                logger.error("Вопрос не найден в базе данных!")
            return question
        except Exception as e:
            logger.error(f"Ошибка при запросе вопроса из базы данных: {e}")
            return None
        finally:
            db.close()

    def prompt_model(self, prompt: Prompt) -> str:
        """
        Отправляет запрос к OpenAI API для генерации текста на основе промпта.

        :param prompt: Объект типа Prompt.
        :return: Сгенерированный текст.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Преобразуем объект Prompt в строку
        prompt_text = prompt.text if hasattr(prompt, "text") else str(prompt)

        # Получаем случайный вопрос из базы данных
        question = self.get_random_question_from_db()

        if not question:
            return "Нет доступных вопросов для задавания."

        # Заменяем {question_text} на конкретный вопрос
        prompt_text = prompt_text.format(question_text=question.text)

        messages = [
            Message(role="system", content=self.system_role),
            Message(role="user", content=prompt_text)  # Используем текст из Prompt
        ]
        body = GptRequest(model=self.chat_model, messages=messages)

        try:
            logger.info("Отправка запроса к OpenAI API...")
            response = requests.post(
                self.chat_api_url,
                headers=headers,
                json=asdict(body)  # Сериализуем тело запроса
            )
            response.raise_for_status()  # Проверка на ошибки HTTP

            response_body = GptResponse(**response.json())
            logger.info("Запрос к OpenAI API выполнен успешно.")
            return response_body.choices[0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к OpenAI API: {e}")
            return f"Ошибка при запросе к OpenAI API: {e}"
        except KeyError as e:
            logger.error(f"Ошибка обработки ответа от OpenAI API: {e}")
            return "Ошибка обработки ответа от OpenAI API"
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return "Неожиданная ошибка при обработке запроса"

    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """
        Отправляет аудиофайл для транскрибации в OpenAI API.

        :param audio_file_path: Путь к аудиофайлу.
        :return: Транскрибированный текст или None в случае ошибки.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            logger.info(f"Отправка аудиофайла {audio_file_path} для транскрибации...")
            with open(audio_file_path, "rb") as audio_file:
                files = {
                    "file": audio_file,
                    "model": (None, self.voice_model),
                    "language": (None, self.language)
                }
                response = requests.post(
                    self.transcription_api_url,
                    headers=headers,
                    files=files
                )
                response.raise_for_status()  # Проверка на ошибки HTTP

                transcription = response.json().get("text", "")
                logger.info("Транскрибация выполнена успешно.")
                return transcription

        except FileNotFoundError:
            logger.error(f"Файл {audio_file_path} не найден.")
            return "Файл не найден"
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к OpenAI API: {e}")
            return f"Ошибка при запросе к OpenAI API: {e}"
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return f"Неожиданная ошибка при транскрибации: {e}"
