from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os


def get_model():
    return OpenAIModel(
        "gpt-5-mini-2025-08-07",
        provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    )