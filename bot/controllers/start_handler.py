from telegram import Update
from bot.services.openai_client import OpenAiClient
from bot.dao.topic_repository import TopicRepository
from bot.models.models import Prompt
from bot.dao.interview_repository import InterviewRepository
from bot.config import Config

async def start_handler(update: Update, context):
    user_name = update.message.from_user.username
    openai_client = OpenAiClient()
    topic_repo = TopicRepository()
    interview_repo = InterviewRepository()
    max_questions = Config.MAX_QUESTIONS

    try:
        interview_repo.clear_user_data(user_name)

        interview_prompt = Prompt.get_prompt_by_name("INTERVIEW_PROMPT")
        # Форматируем текст промпта с количеством вопросов
        welcome_message = openai_client.prompt_model(Prompt(text=interview_prompt.text.format(max_questions=max_questions)))
        await update.message.reply_text(welcome_message)

        await send_next_question(update, context, user_name, openai_client, interview_repo)
        
        print(f"User {user_name} started the interview.")
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text("Произошла ошибка при обработке запроса. Попробуйте позже.")

async def handle_response(update: Update, context):
    user_name = update.message.from_user.username
    user_response = update.message.text
    interview_repo = InterviewRepository()
    
    try:
        interview_repo.add_answer(user_name, user_response)
        await send_next_question(update, context, user_name, OpenAiClient(), interview_repo)
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text("Произошла ошибка при обработке ответа. Попробуйте позже.")

async def send_next_question(update: Update, context, user_name, openai_client, interview_repo):
    try:
        question_prompt = Prompt.get_prompt_by_name("QUESTION_PROMPT")
        next_question = openai_client.prompt_model(question_prompt)
        
        interview_repo.add_question(user_name, next_question)
        await update.message.reply_text(next_question)
    except Exception as e:
        print(f"Error occurred while sending the next question: {e}")
        await update.message.reply_text("Произошла ошибка при получении следующего вопроса. Попробуйте позже.")
        