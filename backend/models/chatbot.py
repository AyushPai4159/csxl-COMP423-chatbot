from pydantic import BaseModel, Field
from public_user import PublicUser
from message_response import ChatMessageResponse

class ChatSession(BaseModel):
    Session_Id: int
    Onyen: str
    User: PublicUser
    User_chats: list[ChatMessageResponse] # Each Tuple is a user prompt followed 
