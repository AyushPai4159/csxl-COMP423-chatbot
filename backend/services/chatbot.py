from typing import List
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService
from ..models.chatbot import ChatSession, ChatMessageResponse


class ChatBotService:
    """Service provides methods to interact with the chatbot API."""

    chat_id_counter = 0

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes new ChatBotService"""
        self._session = session
        self._permission_svc = permission_svc

    def chatbot_response(self, user_prompt: str) -> str:
        # We are sending the user message to the chatbot API and getting a response
        # Step by step
        # 1. We are getting the user message from somewhere(figure out where)
        # 2. We are sending the user message to the chatbot API
        #
        # 3. We are getting the response from the chatbot API

        api_response_c = "Placeholder Chatbot Response!"  # eventually replace with actual API call to chatbot API
        chat_id_c = self.chat_id_counter

        responseModel = ChatMessageResponse(
            chat_id=chat_id_c, user_prompt=user_prompt, api_response=api_response_c
        )
        self.chat_id_counter += 1

        return responseModel.api_response
