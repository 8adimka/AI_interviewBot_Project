from bot.services.dto.question import Question
from bot.dao.interview_repository import InterviewRepository
from bot.dao.topic_repository import TopicRepository

class QuestionService:
    def __init__(self, interview_repository: InterviewRepository, topic_repository: TopicRepository):
        self.interview_repository = interview_repository
        self.topic_repository = topic_repository

    def get_random_topic(self) -> str:
        """
        Возвращает случайную тему.
        """
        return self.topic_repository.get_random_topic()

    def create_question(self, question_text: str, answer_text: str = "") -> Question:
        """
        Создает объект Question.
        """
        return Question(question=question_text, answer=answer_text)

    def add_question(self, user_name: str, question_text: str) -> None:
        """
        Добавляет вопрос пользователя в репозиторий.
        """
        self.interview_repository.add_question(user_name, question_text)

    def add_answer(self, user_name: str, answer_text: str) -> None:
        """
        Добавляет ответ на последний вопрос пользователя.
        """
        self.interview_repository.add_answer(user_name, answer_text)

    def finish_interview(self, user_name: str) -> list[Question]:
        """
        Завершает интервью и возвращает список вопросов и ответов.
        """
        return self.interview_repository.finish_interview(user_name) or []

    def get_user_questions_count(self, user_name: str) -> int:
        """
        Возвращает количество вопросов для пользователя.
        """
        return self.interview_repository.get_user_questions_count(user_name)
    