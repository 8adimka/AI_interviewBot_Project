from dataclasses import dataclass
from typing import List, Any

@dataclass
class Message:
    content: str

@dataclass
class Choice:
    message: Message

@dataclass
class GptResponse:
    choices: List[Choice]
    
    def __init__(self, **kwargs):
        self.choices = kwargs.get('choices', [])
        # Игнорировать другие параметры, такие как 'id'
