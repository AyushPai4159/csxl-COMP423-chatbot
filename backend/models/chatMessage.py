from pydantic import BaseModel, Field
from backend.models.public_user import PublicUser


class ChatMessageResponse(BaseModel):
    chat_id: int
    user_prompt: str
    api_response: str
    session_id: int



    