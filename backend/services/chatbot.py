from typing import List
from fastapi import Depends

from sqlalchemy import select
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService
from ..models.chatMessage import ChatMessageResponse
from ..models.chatSession import ChatSession
from ..entities.chat_message_entity import ChatMessageResponseEnitity
from ..services.openai import OpenAIService
from ..models.openai_chatbot_response import OpenAIChatbotResponse


class ChatBotService:
    """Service provides methods to interact with the chatbot API."""

    chat_id_counter: int
    _openapi_svc_: OpenAIService
    _session: Session

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)],
        openai_svc: Annotated[OpenAIService, Depends()],
    ):
        """Initializes new ChatBotService"""
        self._session = session
        self._openapi_svc_ = openai_svc
        self.chat_id_counter = 0

    def ai_response(self, user_input: str) -> OpenAIChatbotResponse:
        system_prompt = """
        You are a chatbot for the UNC CSXL website at https://csxl.unc.edu. 
        Your job is to answer user questions as a chatbot, only for the CSXL website. 
        If anyone asks about anything different than the CSXL website, please say 'I am sorry, but I can only answer questions about the CSXL website and UNC Chapel Hill questions related to the CS Department.' 
        Try to keep answers short and concise. 
        Here are some other rules.
        Can display the UNC CS Department URL: cs.unc.edu
        Only links allowed are cs.unc.edu and csxl.unc.edu
        Do not provide any other links."""
        user_prompt = user_input
        response_model = OpenAIChatbotResponse
        return self._openapi_svc_.prompt(system_prompt, user_prompt, response_model)

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
            chat_id=chat_id_c, user_prompt=user_prompt, api_response=api_response_c, session_id=1
        )
        self.chat_id_counter += 1


        newEntity = ChatMessageResponseEnitity.from_model(responseModel)
        self._session.add(newEntity)
        self._session.commit()

        return responseModel.api_response
