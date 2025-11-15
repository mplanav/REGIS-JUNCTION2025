from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.chat_mock import mock_chat_reply

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Temporary mock chat endpoint.
    Later, this will call Gemini instead of mock_chat_reply().
    """
    answer = mock_chat_reply(req.message)
    return ChatResponse(answer=answer)
