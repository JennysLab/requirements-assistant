"""
Request-/Response-Modelle. Bewusst so geschnitten, dass sie direkt zu den
Datenformen aus dem Frontend passen (vgl. requirements-assistant-frontend/
src/mock/mockRequirements.js) - das Frontend ergaenzt beim Einlesen nur
noch UI-seitige Felder wie id/key/status, die das Backend nicht kennen muss.
"""
from pydantic import BaseModel, Field


# ---- Chat ---------------------------------------------------------------

class ChatMessageIn(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessageIn]


class ChatResponse(BaseModel):
    reply: str


# ---- Epics (Anforderungs-Workflow, Schritt 1) ----------------------------

class EpicGenerationRequest(BaseModel):
    # Freitext, aus dem Epics abgeleitet werden - z. B. eine
    # Vorhabensbeschreibung, oder (bei "Neu generieren") der aktuelle
    # Epic-Inhalt zur Ueberarbeitung.
    source_text: str = Field(..., min_length=1)
    max_epics: int = Field(default=5, ge=1, le=10)


class GeneratedEpic(BaseModel):
    title: str
    summary: str


class EpicGenerationResponse(BaseModel):
    epics: list[GeneratedEpic]


# ---- Requirements + Akzeptanzkriterien (Schritt 2) -----------------------

class RequirementGenerationRequest(BaseModel):
    epic_title: str
    epic_summary: str
    max_requirements: int = Field(default=4, ge=1, le=8)


class GeneratedRequirement(BaseModel):
    title: str
    description: str
    acceptance_criteria: list[str]


class RequirementGenerationResponse(BaseModel):
    requirements: list[GeneratedRequirement]
