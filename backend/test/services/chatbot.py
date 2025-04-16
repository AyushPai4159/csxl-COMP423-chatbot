"""Mock data for permissions in the system."""

import pytest
from sqlalchemy.orm import Session
from ...entities.chat_message_entity import ChatMessageResponseEnitity
from ...entities.chat_session_entity import ChatSessionEntity




__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"



def insert_fake_data(session: Session):


    chatSessionEntity = ChatSessionEntity(
        session_id=1,
        onyen="stewiestewart",
        user_id=1,
    )

    session.add(chatSessionEntity)

    session.commit()

    chatMessageEntity = ChatMessageResponseEnitity(
        chat_id=1,
        user_prompt="What lovely weather today",
        api_response="N/A",
        session_id=1,
    )
    session.add(chatMessageEntity)

    chatMessageEntity2 = ChatMessageResponseEnitity(
        chat_id=2,
        user_prompt="What not lovely weather today",
        api_response="N/A",
        session_id=1,
    )

    session.add(chatMessageEntity2)



@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
