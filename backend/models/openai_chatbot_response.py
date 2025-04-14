from pydantic import BaseModel


class OpenAIChatbotResponse(BaseModel):
    """Response model for OpenAI chatbot endpoint."""

    chatbot_response: str
