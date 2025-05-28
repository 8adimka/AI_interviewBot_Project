from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.controllers.start_handler import start_handler
from bot.controllers.voice_handler import VoiceHandler
from bot.services.openai_client import OpenAiClient
from bot.dao.interview_repository import InterviewRepository
from bot.dao.topic_repository import TopicRepository
from bot.config import Config

def setup_telegram_bot():
    token = Config.TELEGRAM_BOT_TOKEN
    max_questions = Config.MAX_QUESTIONS
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")

    application = Application.builder().token(token).build()

    # Инициализация зависимостей
    openai_client = OpenAiClient()
    interview_repo = InterviewRepository()
    topic_repo = TopicRepository()
    voice_handler = VoiceHandler(interview_repo, topic_repo, openai_client, max_questions)

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(filters.VOICE, voice_handler.process))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

