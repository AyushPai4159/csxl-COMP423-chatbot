from pydantic import BaseModel, Field
from public_user import PublicUser


class ChatMessageResponse(BaseModel):
    Chat_id: int
    User_prompt: str
    Api_response: str


class ChatSession(BaseModel):
    Session_Id: int
    Onyen: str
    User: PublicUser
    User_chats: list[ChatMessageResponse]  # Each Tuple is a user prompt followed
