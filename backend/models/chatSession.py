from pydantic import BaseModel, Field
from backend.models.public_user import PublicUser




class ChatSession(BaseModel):
    session_id: int
    onyen: str
    user: PublicUser