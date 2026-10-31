"""
POST /api/chat - der allgemeine Assistenz-Chat von der Landing Page.
Ersetzt die Platzhalter-Antwort aus ChatContext.jsx (TODO-Kommentar dort)
durch einen echten LLM-Aufruf.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.config import Settings, get_settings
from app.llm.anthropic_provider import AnthropicProvider
from app.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])

SYSTEM_PROMPT = (
    "Du bist eine KI-Assistenz im Anforderungsmanagement (Requirements Engineering). "
    "Du unterstuetzt Fachanwender:innen (Business Analysts, Product Owner) dabei, "
    "Anforderungen zu verstehen, zu formulieren, zu strukturieren und zu pruefen. "
    "Antworte praezise, sachlich und auf Deutsch."
)


def get_llm_provider(settings: Settings = Depends(get_settings)) -> AnthropicProvider:
    # Dependency Injection: der Endpoint unten kennt nur den Rueckgabetyp
    # der Funktion (AnthropicProvider ist hier zugleich der Port), nicht
    # die interne Client-Erstellung.
    return AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.anthropic_model)


@router.post("", response_model=ChatResponse)
def send_chat_message(
    payload: ChatRequest,
    llm: AnthropicProvider = Depends(get_llm_provider),
) -> ChatResponse:
    if not payload.messages:
        raise HTTPException(status_code=400, detail="messages darf nicht leer sein.")

    anthropic_messages = [{"role": m.role, "content": m.content} for m in payload.messages]
    reply = llm.generate_text(anthropic_messages, system=SYSTEM_PROMPT)
    return ChatResponse(reply=reply)
