from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from bot.database import SessionLocal
from bot.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from bot.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), default="General")  # Категория вопроса
    user_name = Column(String(50), nullable=False)  # Имя пользователя
    text = Column(Text, nullable=False)  # Текст вопроса
    answers = relationship("Answer", back_populates="question", cascade="all, delete", lazy="dynamic")

    def __repr__(self):
        return f"<Question(id={self.id}, category={self.category}, user_name={self.user_name})>"


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)  # Имя пользователя
    text = Column(Text, nullable=False)  # Текст ответа
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)  # Связь с вопросом
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, user_name={self.user_name}, question_id={self.question_id})>"


class Prompt(Base):
    __tablename__ = "prompts"

    name = Column(String(50), primary_key=True)  # Название промпта (например, "QUESTION_PROMPT")
    text = Column(Text, nullable=False)  # Текст промпта

    @staticmethod
    def get_prompt_by_name(name: str) -> "Prompt":
        # Получаем сессию для запроса с контекстным менеджером
        with SessionLocal() as db:
            prompt = db.query(Prompt).filter(Prompt.name == name).first()
            if not prompt:
                raise ValueError(f"Промпт с именем {name} не найден.")
            return prompt

    def to_dict(self):
        return {
            "name": self.name,
            "text": self.text
        }

    def __repr__(self):
        return f"<Prompt(name={self.name})>"
    

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    is_finished = Column(Boolean, default=False)
    finished_at = Column(DateTime, nullable=True)
