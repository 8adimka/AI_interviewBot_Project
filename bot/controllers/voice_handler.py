import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from bot.services.openai_client import OpenAiClient
from bot.dao.interview_repository import InterviewRepository
from bot.dao.topic_repository import TopicRepository
from bot.models.models import Prompt
import os

class VoiceHandler:
    def __init__(
        self,
        interview_repo: InterviewRepository,
        topic_repo: TopicRepository,
        openai_client: OpenAiClient,
        max_questions: int,
    ):
        self.interview_repo = interview_repo
        self.topic_repo = topic_repo
        self.openai_client = openai_client
        self.max_questions = max_questions

    async def process(self, update: Update, context: CallbackContext):
        if not update.message or not update.message.voice:
            await update.message.reply_text("Ошибка: голосовое сообщение не найдено.")
            return

        user_name = update.message.from_user.username or "Unknown"

        try:
            # Скачиваем голосовое сообщение
            file_path = await self.download_voice(update.message.voice.file_id, context)
        except FileNotFoundError as e:
            await update.message.reply_text(f"Ошибка: {e}")
            return
        except Exception as e:
            await update.message.reply_text(f"Ошибка при скачивании файла: {e}")
            return

        try:
            # Транскрибируем голосовое сообщение
            answer_text = await self.transcribe_voice(update, context)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при транскрибации: {e}")
            return

        # Получаем последний вопрос пользователя
        last_question = self.interview_repo.get_last_question(user_name)
        if not last_question:
            await update.message.reply_text("Ошибка: не найден предыдущий вопрос.")
            return

        # Сохраняем ответ пользователя
        try:
            self.interview_repo.add_answer(user_name, last_question.id, answer_text)
        except ValueError as e:
            await update.message.reply_text(f"Ошибка: {e}")
            return

        # Получаем фидбэк на ответ
        feedback_prompt = Prompt.get_prompt_by_name("ANSWER_FEEDBACK_PROMPT")
        if not feedback_prompt:
            await update.message.reply_text("Ошибка: шаблон фидбэка не найден.")
            return

        # Формируем текст для фидбэка
        feedback_text = feedback_prompt.text.format(
            question_text=last_question.text,
            answer_text=answer_text
        )

        try:
            # Получаем фидбэк от OpenAI
            feedback = self.openai_client.prompt_model(Prompt(text=feedback_text))
            await update.message.reply_text(feedback)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при получении фидбэка: {e}")
            return

        # Проверяем, нужно ли задать следующий вопрос или завершить интервью
        if self.interview_repo.get_user_questions_count(user_name) >= self.max_questions:
            # Даем общий фидбэк
            final_feedback_prompt = Prompt.get_prompt_by_name("FEEDBACK_PROMPT")
            if not final_feedback_prompt:
                await update.message.reply_text("Ошибка: шаблон общего фидбэка не найден.")
                return

            # Получаем все ответы пользователя
            try:
                answers = self.interview_repo.finish_interview(user_name)
                if not answers:
                    await update.message.reply_text("Ошибка: ответы пользователя не найдены.")
                    return

                answers_text = "\n".join([f"Вопрос: {a.question.text}\nОтвет: {a.text}" for a in answers])
            except ValueError as e:
                await update.message.reply_text(f"Ошибка: {e}")
                return

            # Формируем текст для общего фидбэка
            final_feedback_text = final_feedback_prompt.text.format(answers_text=answers_text)

            try:
                # Получаем общий фидбэк от OpenAI
                final_feedback = self.openai_client.prompt_model(Prompt(text=final_feedback_text))
                await update.message.reply_text(final_feedback)
            except Exception as e:
                await update.message.reply_text(f"Ошибка при получении общего фидбэка: {e}")
                return

            # Завершаем интервью
            self.interview_repo.mark_interview_finished(user_name)
            await update.message.reply_text("Интервью завершено. Спасибо за участие!")
        else:
            # Задаем следующий вопрос
            next_question = self.ask_next_question(user_name)
            await update.message.reply_text(next_question)

    async def transcribe_voice(self, update: Update, context: CallbackContext) -> str:
        voice = update.message.voice
        file_id = voice.file_id
        file_path = await self.download_voice(file_id, context)
        transcription = self.openai_client.transcribe(file_path)
        
        if "Ошибка" in transcription:
            raise Exception(transcription)
        
        return transcription

    async def download_voice(self, file_id: str, context: CallbackContext) -> str:
        file = await context.bot.get_file(file_id)  # Получаем объект File
        file_path = f"/tmp/{file_id}.ogg"
        
        # Скачиваем файл асинхронно
        await file.download_to_drive(file_path)
        
        # Проверяем, что файл существует
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не был сохранен.")
        
        return file_path

    def ask_next_question(self, user_name: str) -> str:
        prompt_obj = Prompt.get_prompt_by_name("QUESTION_PROMPT")
        if not prompt_obj:
            return "Ошибка: шаблон вопроса не найден."

        # Получаем случайный вопрос из базы данных
        question = self.openai_client.get_random_question_from_db()
        if not question:
            return "Ошибка: не найдены вопросы в базе данных."

        # Заменяем {question_text} на конкретный вопрос
        prompt_text = prompt_obj.text.format(question_text=question.text)

        # Генерируем вопрос с помощью OpenAI
        generated_question = self.openai_client.prompt_model(Prompt(text=prompt_text))
        
        if not generated_question or "Ошибка" in generated_question:
            return "Ошибка: не удалось сформулировать вопрос."

        # Сохраняем вопрос в базе данных
        self.interview_repo.add_question(user_name, generated_question)

        return generated_question
    