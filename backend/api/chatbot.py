"""Chatbot API

Chatbot routes are used to interact with the chatbot
"""

from fastapi import APIRouter, Depends
from backend.models.chatSession import ChatSession
from backend.models.chatMessage import ChatMessageResponse
from typing import List
from backend.services.chatbot import ChatBotService
from ..models.openai_chatbot_response import OpenAIChatbotResponse
from ..models.user import User
from ..api.authentication import registered_user


openapi_tags = {
    "name": "Chatbot",
    "description": "Chat, view, update, and delete chat logs and history.",
}

api = APIRouter(prefix="/api/chatbot")


@api.post("/chat", tags=["Chatbot"])
def chat(
    request: ChatMessageResponse, chatbot_service: ChatBotService = Depends()
) -> str:
    """
    Send a message to the chatbot api and receive a response
    """
    return chatbot_service.ai_response(request)


@api.post("/create/chat", tags=["Chatbot"])
def createChat(chatbot_service: ChatBotService = Depends()) -> str:
    """
    Send a message to the chatbot api and receive a response
    """
    return chatbot_service.create_new_session()


@api.get("/admin/session/{session_id}", tags=["Chatbot"])
def get_session_history(
    session_id: int, chatbot_service: ChatBotService = Depends()
) -> list[ChatMessageResponse]:
    """
    Get the chat session history for a given session id
    """
    return chatbot_service.get_all_sessionMessages(session_id)


@api.get("/admin/sessions/", tags=["Chatbot"])
def get_available_sessions(chatbot_service: ChatBotService = Depends()) -> list[int]:
    """
    Get the chat session history for a given session id
    """
    return chatbot_service.get_all_sessions()


@api.delete("/admin/session/{session_id}", tags=["Chatbot"])
def delete_session(session_id: int, chatbot_service: ChatBotService = Depends()):
    """
    Delete a chat session history
    """
    return chatbot_service.delete_session(session_id)
