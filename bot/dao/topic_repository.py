from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from bot.models.models import Question
from bot.database import get_db

class TopicRepository:
    def __init__(self):
        self.db: Session = next(get_db())

    def get_random_topic(self) -> str:
        question = self.db.query(Question).order_by(func.random()).first()
        if not question:
            raise ValueError("В базе данных нет вопросов.")
        return question.text
    