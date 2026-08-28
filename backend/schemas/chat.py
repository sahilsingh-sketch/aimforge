from pydantic import BaseModel
from typing import List

class ChatMessageSchema(BaseModel):
    role: str
    content: str
    timestamp: int

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: ChatMessageSchema
