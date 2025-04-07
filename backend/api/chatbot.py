"""Chatbot API

Chatbot routes are used to interact with the chatbot
"""

from fastapi import APIRouter, Depends
from backend.models.chatbot import ChatSession, ChatMessageResponse
from typing import List
from backend.services.chatbot import ChatBotService


openapi_tags = {
    "name": "Chatbot",
    "description": "Chat, view, update, and delete chat logs and history.",
}

api = APIRouter(prefix="/api/chatbot")


@api.post("/chat", tags=["Chatbot"])
def chat(user_message: str, chatbot_service: ChatBotService = Depends()) -> str:
    """
    Send a message to the chatbot api and receive a response
    """
    return chatbot_service.chatbot_response(user_message)


@api.get("/admin/session/{session_id}", tags=["Chatbot"])
def get_session_history(session_id: int) -> ChatSession:
    """
    Get the chat session history for a given session id
    """
    return


@api.patch("/admin/session/{session_id}", tags=["Chatbot"])
def update_session_history(session_id: int, chat_session: ChatSession):
    """
    Update the chat session history for a given session id
    """
    return None


@api.patch("/admin/session/{session_id}/{chat_index}", tags=["Chatbot"])
def update_chat_message(
    session_id: int, chat_index: int, chat_message: ChatMessageResponse
):
    """
    Update a specific chat message in a chat session history
    """
    return None


@api.delete("/admin/session/{session_id}", tags=["Chatbot"])
def delete_session(session_id: int):
    """
    Delete a chat session history
    """
    return None
