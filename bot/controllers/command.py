from abc import ABC, abstractmethod
from telegram import Update
from bot.services.gpt_client import GPTClient
from bot.dao.question_dao import QuestionDAO
from bot.dao.answer_dao import AnswerDAO

class Command(ABC):
    def __init__(self, question_dao: QuestionDAO, answer_dao: AnswerDAO, gpt_client: GPTClient):
        self.question_dao = question_dao
        self.answer_dao = answer_dao
        self.gpt_client = gpt_client

    @abstractmethod
    def is_applicable(self, update: Update) -> bool:
        """Определяет, применяется ли команда к данному обновлению"""
        pass

    @abstractmethod
    def process(self, update: Update) -> str:
        """Обрабатывает команду и возвращает ответ"""
        pass
