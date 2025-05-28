from sqlalchemy.orm import Session
from bot.models.models import Prompt
from bot.database import get_db

class PromptDAO:
    @staticmethod
    def get_prompt_by_name(name: str) -> str:
        db: Session = next(get_db())
        prompt = db.query(Prompt).filter(Prompt.name == name).first()
        if not prompt:
            raise ValueError(f"Prompt with name '{name}' not found.")
        return prompt.text
    
    