from pydantic import BaseModel, Field
from backend.models.public_user import PublicUser


class ChatMessageResponse(BaseModel):
    chat_id: int
    user_prompt: str
    api_response: str


class ChatSession(BaseModel):
    session_id: int
    onyen: str
    user: PublicUser
    user_chats: list[ChatMessageResponse]  # Each Tuple is a user prompt followed
