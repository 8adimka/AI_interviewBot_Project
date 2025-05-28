from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    role: str
    content: str

@dataclass
class GptRequest:
    model: str
    messages: List[Message]
    