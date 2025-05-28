from datetime import datetime
from sqlalchemy.orm import Session
from bot.models.models import Question, Answer, Interview
from bot.database import get_db

class InterviewRepository:
    def __init__(self):
        self.db: Session = next(get_db())

    def add_question(self, user_name: str, question_text: str):
        question = Question(user_name=user_name, text=question_text)
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def get_user_questions_count(self, user_name: str) -> int:
        return (
            self.db.query(Question)
            .filter(Question.user_name == user_name)
            .count()
        )
    
    def get_last_question(self, user_name: str):
        return (
            self.db.query(Question)
            .filter(Question.user_name == user_name)
            .order_by(Question.id.desc())
            .first()
        )

    def add_answer(self, user_name: str, question_id: int, answer_text: str):
        # Проверяем, что вопрос существует
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError(f"Вопрос с ID {question_id} не найден.")

        answer = Answer(user_name=user_name, question_id=question_id, text=answer_text)
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def get_user_questions(self, user_name: str):
        return self.db.query(Question).filter(Question.user_name == user_name).all()
    
    def finish_interview(self, user_name: str) -> list[Answer]:
        """
        Завершает интервью и возвращает список ответов пользователя вместе с вопросами.
        """
        answers = (
            self.db.query(Answer)
            .join(Question, Answer.question_id == Question.id)
            .filter(Answer.user_name == user_name)
            .all()
        )
        if not answers:
            raise ValueError(f"Ответы для пользователя {user_name} не найдены.")
        
        return answers
    
    def mark_interview_finished(self, user_name: str) -> None:
        """
        Помечает интервью как завершенное.
        """
        interview = self.db.query(Interview).filter(Interview.user_name == user_name).first()
        if not interview:
            interview = Interview(user_name=user_name, is_finished=True, finished_at=datetime.now())
            self.db.add(interview)
        else:
            interview.is_finished = True
            interview.finished_at = datetime.now()
        self.db.commit()

    def clear_user_data(self, user_name: str):
        """
        Удаляет все вопросы и ответы пользователя перед началом нового интервью.
        """
        self.db.query(Answer).filter(Answer.user_name == user_name).delete()
        self.db.query(Question).filter(Question.user_name == user_name).delete()
        self.db.commit()
        