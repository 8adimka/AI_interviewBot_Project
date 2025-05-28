from sqlalchemy.orm import Session
from bot.models.models import Question
from bot.database import get_db

class QuestionDAO:
    @staticmethod
    def get_first_question():
        db: Session = next(get_db())
        return db.query(Question).first()

