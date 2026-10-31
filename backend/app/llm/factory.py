"""
Fabrik fuer den Sprachmodell-Anbieter: der EINE Ort, der den konkreten
Anbieter kennt. Anderer Anbieter (OpenAI, Bedrock, On-Premise) = hier tauschen.
"""
from fastapi import Depends

from app.config import Settings, get_settings

from .anthropic_provider import AnthropicProvider
from .base import LLMProvider


def get_llm(settings: Settings = Depends(get_settings)) -> LLMProvider:
    return AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.anthropic_model)
