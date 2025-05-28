from django.http import JsonResponse
from django.views import View
from telegram import Update
from bot.telegram_config import setup_telegram_bot
import json

class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        # Парсим входящее обновление от Telegram
        update = Update.de_json(json.loads(request.body), None)
        
        # Обрабатываем обновление
        setup_telegram_bot()  # Инициализация бота
        return JsonResponse({"status": "ok"})
    