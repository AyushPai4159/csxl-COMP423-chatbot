from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.chatbot import ChatMessageResponse


class ChatMessageResponseEnitity(EntityBase):
    __tablename__ = "chat_message_response"

    chat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_prompt: Mapped[str] = mapped_column(String(1000), nullable=False)
    api_response: Mapped[str] = mapped_column(String(1000), nullable=False)

    def to_model(self) -> ChatMessageResponse:
        return ChatMessageResponse(
            Chat_id=self.chat_id,
            User_prompt=self.user_prompt,
            Api_response=self.api_response,
        )

    @classmethod
    def from_model(cls, model: ChatMessageResponse) -> Self:
        return cls(
            chat_id=model.Chat_id,
            user_prompt=model.User_prompt,
            api_response=model.Api_response,
        )
