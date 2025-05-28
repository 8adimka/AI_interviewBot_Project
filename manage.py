import os
import sys

from bot.database import init_db
from bot.telegram_config import setup_telegram_bot

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from bot.management.commands.add_initial_data import Command

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Добавление начальных данных
    command = Command()
    command.handle()

    # Запуск Telegram бота
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")
    setup_telegram_bot()

