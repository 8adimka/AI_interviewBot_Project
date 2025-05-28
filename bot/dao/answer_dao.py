from sqlalchemy.orm import Session
from bot.models.models import Answer
from bot.database import get_db

class AnswerDAO:
    @staticmethod
    def add_answer(question_id: int, text: str):
        db: Session = next(get_db())
        answer = Answer(question_id=question_id, text=text)
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer

    @staticmethod
    def get_answer_by_question_id(question_id: int):
        db: Session = next(get_db())
        return db.query(Answer).filter(Answer.question_id == question_id).first()
    
    