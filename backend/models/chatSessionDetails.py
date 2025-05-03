from .chatMessage import ChatMessageResponse
from .chatSession import ChatSession


class ChatSessionDetails(ChatSession):
    messages: list[ChatMessageResponse]
