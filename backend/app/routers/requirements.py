"""
POST /api/requirements/epics   - Epics aus einem Text ableiten
POST /api/requirements/details - Anforderungen + Akzeptanzkriterien zu einem Epic ableiten

Beide nutzen generate_structured() statt generate_text(): Freitext vom
Modell muesste man fehleranfaellig parsen (Ueberschriften, Aufzaehlungen,
Formatierung koennen variieren). Die erzwungene Tool-Nutzung garantiert
stattdessen valides JSON passend zum jeweiligen Schema.

Diese Endpoints bedienen zwei Stellen im Frontend:
  - RequirementsContext.jsx -> regenerateEpic()         -> /epics
  - RequirementsContext.jsx -> regenerateRequirement()   -> /details
("Neu generieren"-Button auf EpicCard bzw. RequirementCard)
"""
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.llm.anthropic_provider import AnthropicProvider
from app.schemas import (
    EpicGenerationRequest,
    EpicGenerationResponse,
    RequirementGenerationRequest,
    RequirementGenerationResponse,
)

router = APIRouter(prefix="/api/requirements", tags=["requirements"])

RE_SYSTEM_PROMPT = (
    "Du bist Requirements-Engineering-Experte. Du leitest aus einer "
    "Vorhabensbeschreibung strukturierte Epics ab bzw. aus einem Epic konkrete, "
    "pruefbare Anforderungen mit Akzeptanzkriterien. Anforderungen formulierst du "
    "im Format 'Als <Rolle> moechte ich <Ziel>, damit <Nutzen>.'. Antworte "
    "ausschliesslich auf Deutsch und ausschliesslich ueber den bereitgestellten "
    "Funktionsaufruf (kein zusaetzlicher Freitext)."
)

EPIC_SCHEMA = {
    "type": "object",
    "properties": {
        "epics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Kurzer, praegnanter Epic-Titel"},
                    "summary": {
                        "type": "string",
                        "description": "2-4 Saetze Zusammenfassung auf Epic-Ebene",
                    },
                },
                "required": ["title", "summary"],
            },
        }
    },
    "required": ["epics"],
}

REQUIREMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "acceptance_criteria": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "3-5 pruefbare Akzeptanzkriterien",
                    },
                },
                "required": ["title", "description", "acceptance_criteria"],
            },
        }
    },
    "required": ["requirements"],
}


def get_llm_provider(settings: Settings = Depends(get_settings)) -> AnthropicProvider:
    return AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.anthropic_model)


@router.post("/epics", response_model=EpicGenerationResponse)
def generate_epics(
    payload: EpicGenerationRequest,
    llm: AnthropicProvider = Depends(get_llm_provider),
) -> EpicGenerationResponse:
    prompt = (
        f"Leite maximal {payload.max_epics} Epic(s) aus folgender Beschreibung ab:\n\n"
        f"{payload.source_text}"
    )
    result = llm.generate_structured(
        messages=[{"role": "user", "content": prompt}],
        tool_name="return_epics",
        tool_description="Gibt eine Liste generierter Epics zurueck.",
        input_schema=EPIC_SCHEMA,
        system=RE_SYSTEM_PROMPT,
    )
    return EpicGenerationResponse(**result)


@router.post("/details", response_model=RequirementGenerationResponse)
def generate_requirements(
    payload: RequirementGenerationRequest,
    llm: AnthropicProvider = Depends(get_llm_provider),
) -> RequirementGenerationResponse:
    prompt = (
        f"Leite maximal {payload.max_requirements} konkrete Anforderung(en) inkl. "
        f"Akzeptanzkriterien fuer folgendes Epic ab:\n\n"
        f"Titel: {payload.epic_title}\nZusammenfassung: {payload.epic_summary}"
    )
    result = llm.generate_structured(
        messages=[{"role": "user", "content": prompt}],
        tool_name="return_requirements",
        tool_description="Gibt eine Liste generierter Anforderungen zurueck.",
        input_schema=REQUIREMENT_SCHEMA,
        system=RE_SYSTEM_PROMPT,
    )
    return RequirementGenerationResponse(**result)
