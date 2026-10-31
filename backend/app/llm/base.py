"""
LLMProvider: der "Port" aus der Ports-and-Adapters-Architektur, die im
Expose unter Kapitel 5.9/5.11 als Designentscheidung begruendet ist
("LLM muss austauschbar sein"). Der Rest der Anwendung (die Router in
app/routers/) kennt ausschliesslich dieses Interface, nie eine konkrete
Provider-Bibliothek.

Ein Wechsel zu einem anderen Anbieter (Amazon Bedrock, Mistral, Aleph
Alpha, ein lokal via Ollama gehostetes Modell fuer On-Premise-Betrieb...)
bedeutet: eine neue Klasse schreiben, die dieses Interface erfuellt, und
sie in den Routern anstelle von AnthropicProvider einsetzen. Kein Code
ausserhalb von app/llm/ muss sich dafuer aendern.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class LLMProvider(ABC):
    @abstractmethod
    def generate_text(
        self,
        messages: list[dict[str, str]],
        system: Optional[str] = None,
    ) -> str:
        """Freier Chat: Nachrichtenverlauf rein, Antworttext raus.
        Wird vom /api/chat-Endpoint verwendet."""
        raise NotImplementedError

    @abstractmethod
    def generate_structured(
        self,
        messages: list[dict[str, str]],
        tool_name: str,
        tool_description: str,
        input_schema: dict[str, Any],
        system: Optional[str] = None,
    ) -> dict[str, Any]:
        """Erzwingt eine Ausgabe, die exakt zu input_schema (JSON Schema)
        passt - z. B. eine Liste von Epics oder Anforderungen als valides
        JSON statt als Freitext, den man fehleranfaellig parsen muesste.
        Wird von /api/requirements/* verwendet."""
        raise NotImplementedError
