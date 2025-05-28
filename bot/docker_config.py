import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_TRANSCRIPTION_URL = os.getenv("OPENAI_TRANSCRIPTION_URL", "https://api.openai.com/v1/audio/transcriptions")
    OPENAI_TRANSCRIPTION_MODEL = os.getenv("OPENAI_TRANSCRIPTION_MODEL", "whisper-1")
    OPENAI_TRANSCRIPTION_LANGUAGE = os.getenv("OPENAI_TRANSCRIPTION_LANGUAGE", "en")
    OPENAI_CHAT_URL = os.getenv("OPENAI_CHAT_URL", "https://api.openai.com/v1/chat/completions")
    OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
    OPENAI_SYSTEM_ROLE = os.getenv("OPENAI_SYSTEM_ROLE", "You are a helpful assistant.")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://v:1111@db/interview_db") 

    MAX_QUESTIONS = 4
