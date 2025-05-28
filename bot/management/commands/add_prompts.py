from django.core.management.base import BaseCommand
from bot.models.models import Prompt
from bot.database import SessionLocal

class Command(BaseCommand):
    help = "Добавляет начальные промпты в базу данных"

    def handle(self, *args, **kwargs):
        db = SessionLocal()

        prompts = [
            {
                "name": "QUESTION_PROMPT", 
                "text": """
                    Вот исходный вопрос для собеседования на Python Junior: {question_text}
                    Задай его, придумав интересную ситуацию с каким-нибудь реальным известным
                    приложением, в контексте которого и будет задаваться вопрос.
                    Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                """
            },
            {
                "name": "FEEDBACK_PROMPT", 
                "text": """
                    Проанализируй вопросы на собеседовании для позиции Junior Python Developer и те ответы, которые на каждый
                    из них дал кандидат. Давай обратную связь по его ответам.
                """
            },
            {
                "name": "INTERVIEW_PROMPT", 
                "text": """
                    Весело и тепло поприветствуй кандидата на собеседовании, а также расскажи ему о правилах интервью.
                    Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                """
            }
        ]

        for prompt_data in prompts:
            # Проверяем, существует ли уже промпт с таким именем
            existing_prompt = db.query(Prompt).filter_by(name=prompt_data["name"]).first()
            if not existing_prompt:
                prompt = Prompt(name=prompt_data["name"], text=prompt_data["text"])
                db.add(prompt)

        db.commit()
        db.close()
        self.stdout.write(self.style.SUCCESS("Промпты успешно добавлены в базу данных!"))
