from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.chatMessage import ChatMessageResponse
from ..entities.chat_session_entity import ChatSessionEntity




class ChatMessageResponseEnitity(EntityBase):
    __tablename__ = "chat_message_response"

    chat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_prompt: Mapped[str] = mapped_column(String(1000), nullable=False)
    api_response: Mapped[str] = mapped_column(String(), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.session_id"))
    session: Mapped['ChatSessionEntity'] = relationship(back_populates="message")

    def to_model(self) -> ChatMessageResponse:
        return ChatMessageResponse(
            chat_id=self.chat_id,
            user_prompt=self.user_prompt,
            api_response=self.api_response,
            session_id=self.session_id
        )

    @classmethod
    def from_model(cls, model: ChatMessageResponse) -> Self:
        return cls(
            chat_id=model.chat_id,
            user_prompt=model.user_prompt,
            api_response=model.api_response,
            session_id=model.session_id
        )
