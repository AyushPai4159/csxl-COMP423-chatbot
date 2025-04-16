from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.chatSession import ChatSession
# from ..entities.chat_message_entity import ChatMessageResponseEnitity


class ChatSessionEntity(EntityBase):
    __tablename__ = "chat_session"

    session_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    onyen: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)

    message: Mapped[list['ChatMessageResponseEnitity']] = relationship(back_populates="session")
    


    def to_model(self) -> ChatSession:
        return ChatSession(
            Session_Id=self.session_id, Onyen=self.onyen, User=self.user_id
        )

    @classmethod
    def from_model(cls, model: ChatSession) -> Self:
        return cls(session_id=model.Session_Id, onyen=model.Onyen, user_id=model.User)
