from pydantic import BaseModel
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    language: str = "es"
    user_email: str | None = None
    timestamp: str | None = None

class ChatResponse(BaseModel):
    message: str
    timestamp: str
    language: str
