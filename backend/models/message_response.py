
from pydantic import BaseModel, Field


class ChatMessageResponse(BaseModel):
    Chat_id: int
    User_prompt: str
    Api_response: str
