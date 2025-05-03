"""Mock data for permissions in the system."""

import pytest
from ...entities.chat_message_entity import ChatMessageResponseEnitity
from ...entities.chat_session_entity import ChatSessionEntity
from sqlalchemy.orm import Session
from ...services.event import EventService
from ...services.organization import OrganizationService
from ...services.academics.course_site import CourseSiteService
from unittest.mock import MagicMock
from .chatbot_data import fake_data_fixture
from ...services.chatbot import ChatBotService
from ...models.chatMessage import ChatMessageResponse
from ...models.user import User


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture
def mock_dependencies():
    session = MagicMock()
    openai_svc = MagicMock()
    orgs = MagicMock()
    events = MagicMock()
    rooms = MagicMock()
    courses = MagicMock()

    session.query().count.return_value = 0

    return {
        "session": session,
        "openai_svc": openai_svc,
        "orgs": orgs,
        "events": events,
        "rooms": rooms,
        "courses": courses,
    }


@pytest.fixture
def chatbot(session: Session, mock_dependencies: dict[str, MagicMock]):
    return ChatBotService(
        session=session,
        openai_svc=mock_dependencies["openai_svc"],
        organizations=mock_dependencies["orgs"],
        events=mock_dependencies["events"],
        rooms=mock_dependencies["rooms"],
        courses=mock_dependencies["courses"],
    )


def test_chatbot_response_saves_and_returns(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if the openai service gets called and returns a message"""
    mock_dependencies["openai_svc"].prompt.return_value.chatbot_response = "Hello!"
    request = ChatMessageResponse(
        chat_id=0, user_prompt="Hi", api_response="", session_id=1
    )
    subject = User()

    response = chatbot.ai_response(request, subject)

    assert response == "Hello!"


def test_get_all_session_messages(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if we get all the messages from a session"""
    result = chatbot.get_all_sessionMessages(1)
    assert len(result) == 2


def test_format_session_messages(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if the user messages are formated correctly to be re-fed into the ai system prompt"""

    result = chatbot.format_sessionMessages(1)
    assert (
        result
        == "User: What lovely weather today\nChatbot: N/A\nUser: What not lovely weather today\nChatbot: N/A\n"
    )


def test_get_all_sessions(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if the session gets all of the correct ChatSessions and their values"""

    result = chatbot.get_all_sessions()
    assert result == [1]


def test_create_new_session(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if we created a new session given the message with incremented number returned"""
    result = chatbot.create_new_session()
    assert result == "Session 2 created!"


def test_delete_session(
    chatbot: ChatBotService, mock_dependencies: dict[str, MagicMock]
):
    """Tests if we have deleted the session given the returned message of the target value"""
    result = chatbot.delete_session(3)
    assert result == "Session 3 messages deleted!"
