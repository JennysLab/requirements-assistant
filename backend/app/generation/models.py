"""
Datenmodelle der Generierung (Anfragen, Antworten, Template-Beschreibung).

Das Template kommt als Daten vom Frontend: Es beschreibt, welche Felder ein
Epic und eine Anforderung haben. Daraus baut das Backend das Ausgabeschema
und den Feldabschnitt im Prompt. Ein anderes Template ergibt so ein anderes
Ergebnis, ohne dass Code geaendert wird (Anforderung A2.5).
"""
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class FieldDef(BaseModel):
    key: str = Field(..., pattern=r"^[a-zA-Z][a-zA-Z0-9_]{0,30}$")
    label: str
    type: Literal["text", "textarea", "select"] = "text"
    options: Optional[List[str]] = None
    hint: Optional[str] = None


class TemplateDef(BaseModel):
    name: str = ""
    epic: List[FieldDef] = Field(..., min_length=1)
    requirement: List[FieldDef] = Field(..., min_length=1)


class Attachment(BaseModel):
    name: str
    text: str = ""


class _Base(BaseModel):
    input: str = Field(..., min_length=1)
    attachments: List[Attachment] = []
    template: TemplateDef
    # Soll die Wissensbasis als Hintergrund einbezogen werden?
    use_knowledge: bool = True


class EpicsRequest(_Base):
    count: int = Field(default=3, ge=1, le=8)
    # Gesetzt bei "Neu generieren": der bisherige Entwurf wird ueberarbeitet.
    revise: Optional[Dict[str, str]] = None


class RequirementsRequest(_Base):
    epic: Dict[str, str]
    count: int = Field(default=2, ge=1, le=6)
    revise: Optional[Dict[str, str]] = None


class CriteriaRequest(_Base):
    epic: Dict[str, str]
    requirement: Dict[str, str]
    count: int = Field(default=4, ge=1, le=8)


class EpicsResponse(BaseModel):
    epics: List[Dict[str, str]]
    sources: List[Dict[str, Any]] = []


class RequirementsResponse(BaseModel):
    requirements: List[Dict[str, str]]
    sources: List[Dict[str, Any]] = []


class CriteriaResponse(BaseModel):
    criteria: List[str]
    sources: List[Dict[str, Any]] = []
