"""
AnthropicProvider: der aktuell einzige Adapter fuer den LLMProvider-Port
(siehe base.py). Kapselt alles, was Anthropic-spezifisch ist - Client-
Initialisierung, das Format der messages.create()-Aufrufe, wie Text vs.
strukturierte Antworten extrahiert werden. Nichts davon "leakt" nach
aussen; die Router sehen nur generate_text()/generate_structured().
"""
from typing import Any, Optional

from anthropic import Anthropic

from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, max_tokens: int = 4096):
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY fehlt. Bitte .env-Datei anlegen (siehe .env.example) "
                "und einen gueltigen Key eintragen."
            )
        self._client = Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    def generate_text(
        self,
        messages: list[dict[str, str]],
        system: Optional[str] = None,
    ) -> str:
        kwargs: dict[str, Any] = {}
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=messages,
            **kwargs,
        )
        # Content besteht aus Bloecken (Text, ggf. Tool-Use); hier
        # interessieren nur die Text-Bloecke.
        return "".join(block.text for block in response.content if block.type == "text")

    def generate_structured(
        self,
        messages: list[dict[str, str]],
        tool_name: str,
        tool_description: str,
        input_schema: dict[str, Any],
        system: Optional[str] = None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {}
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=messages,
            tools=[
                {
                    "name": tool_name,
                    "description": tool_description,
                    "input_schema": input_schema,
                }
            ],
            # tool_choice erzwingt den Aufruf genau dieses einen Tools.
            # Das ist der etablierte Mechanismus, um garantiert zu
            # input_schema passendes JSON zu bekommen, statt auf sauber
            # formatierten Freitext zu hoffen (siehe Anthropic-Doku zu
            # "Tool Use" / "Structured Outputs").
            tool_choice={"type": "tool", "name": tool_name},
            **kwargs,
        )
        for block in response.content:
            if block.type == "tool_use":
                return block.input
        raise RuntimeError(
            "Das Modell hat keinen tool_use-Block zurückgegeben - das sollte bei "
            "erzwungenem tool_choice nicht passieren. Bitte Prompt/Schema prüfen."
        )
