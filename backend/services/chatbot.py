from typing import List
from fastapi import Depends

from sqlalchemy import select, func, delete
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import db_session
from .permission import PermissionService
from ..models.chatMessage import ChatMessageResponse
from ..models.chatSession import ChatSession
from ..entities.chat_message_entity import ChatMessageResponseEnitity
from ..entities.chat_session_entity import ChatSessionEntity
from ..services.openai import OpenAIService
from ..models.openai_chatbot_response import OpenAIChatbotResponse
from ..services.organization import OrganizationService
from ..services.room import RoomService
from ..services.event import EventService
from ..models.user import User
from ..models.pagination import EventPaginationParams, Paginated, PaginationParams
from ..services.academics.course_site import CourseSiteService


class ChatBotService:
    """Service provides methods to interact with the chatbot API."""

    chat_id_counter: int
    _openapi_svc_: OpenAIService
    _session: Session
    _organizations: OrganizationService
    _rooms: RoomService
    _events: EventService
    _courses: CourseSiteService

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)],
        openai_svc: Annotated[OpenAIService, Depends()],
        organizations: Annotated[OrganizationService, Depends()],
        events: Annotated[EventService, Depends()],
        rooms: Annotated[RoomService, Depends()],
        courses: Annotated[CourseSiteService, Depends()],
    ):
        """Initializes new ChatBotService"""
        self._session = session
        self._openapi_svc_ = openai_svc
        self.chat_id_counter = session.query(ChatMessageResponseEnitity).count()
        self._organizations = organizations
        self._events = events
        self._rooms = rooms
        self._courses = courses

    def ai_response(self, request: ChatMessageResponse) -> str:
        system_prompt = f"""
        You are a chatbot for the UNC CSXL website at https://csxl.unc.edu. 
        At the beginning of being called, check the website to find the latest information, and use that information in your responses.
        Your job is to answer user questions as a chatbot, only for the CSXL website. 
        Your jobs is to also recall previous messages in the chat session.
        If anyone asks about anything unrelated to the University of North Carolina at Chapel Hill or CSXL, please say 'I am sorry, but I can only answer questions about the CSXL website and UNC Chapel Hill questions related to the CS Department.' 
        Try to keep answers short and concise. 
        Here are some other rules.
        Can display the UNC CS Department URL: cs.unc.edu
        Only links allowed are cs.unc.edu and csxl.unc.edu
        Do not provide any other links.
        Physical location/address: Sitterson Hall, 232 S Columbia St, Chapel Hill, NC 27514. Room 156.
        
        """

        user_prompt = request.user_prompt
        response_model = OpenAIChatbotResponse
        returned = "Hello, this is an automated response since I don't own an API key anymore! Please use your imagination for now given my budget cuts."
        # now we have the response_model with the response
        request.api_response = returned
        self.chat_id_counter += 1
        request.chat_id = self.chat_id_counter
        responseModel = ChatMessageResponse(
            chat_id=request.chat_id,
            user_prompt=user_prompt,
            api_response=request.api_response,
            session_id=request.session_id,
        )

        newEntity = ChatMessageResponseEnitity.from_model(responseModel)
        self._session.add(newEntity)
        self._session.commit()
        return request.api_response

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
            chat_id=chat_id_c,
            user_prompt=user_prompt,
            api_response=api_response_c,
            session_id=1,
        )
        self.chat_id_counter += 1

        newEntity = ChatMessageResponseEnitity.from_model(responseModel)
        self._session.add(newEntity)
        self._session.commit()

        return responseModel.api_response

    def get_all_sessionMessages(self, id: int) -> list[ChatMessageResponse]:

        try:
            stmt = select(ChatMessageResponseEnitity).where(
                ChatMessageResponseEnitity.session_id == id
            )
            list = self._session.execute(stmt).scalars().all()
            return list
        except Exception:
            raise Exception("something went wrong")

    def format_sessionMessages(self, id: int) -> str:
        try:
            list = self.get_all_sessionMessages(id)
            if not list:
                return "No messages found for this session."
            formatted = ""
            for message in list:
                formatted += f"User: {message.user_prompt}\n"
                formatted += f"Chatbot: {message.api_response}\n"
            return formatted
        except Exception:
            raise Exception("something went wrong")

    def get_all_sessions(self) -> list[int]:
        try:
            stmt = select(ChatSessionEntity.session_id)
            list = self._session.execute(stmt).scalars().all()
            return list
        except Exception:
            raise Exception("something went wrong")

    def create_new_session(self) -> str:
        maxVal = self._session.execute(
            select(func.max(ChatSessionEntity.session_id))
        ).scalar()
        chatSessionEntity = ChatSessionEntity(
            session_id=maxVal + 1,
            onyen="stewiestewart",
            user_id=1,
        )
        self._session.add(chatSessionEntity)
        self._session.commit()

        return f"Session {maxVal+1} created!"

    def delete_session(self, id: int) -> str:
        try:
            stmt = delete(ChatMessageResponseEnitity).where(
                ChatMessageResponseEnitity.session_id == id
            )
            self._session.execute(stmt)
            self._session.commit()
            return f"Session {id} messages deleted!"
        except Exception:
            raise Exception("something went wrong")
