"""
API-Adressen der Generierung (Modul M2):
  POST /api/generate/epics
  POST /api/generate/requirements
  POST /api/generate/criteria
Die Router enthalten keine Fachlogik, sie reichen an den Orchestrator weiter.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.knowledge.router import get_kb
from app.knowledge.store import KnowledgeBase
from app.llm.base import LLMProvider
from app.llm.factory import get_llm

from .models import (
    CriteriaRequest,
    CriteriaResponse,
    EpicsRequest,
    EpicsResponse,
    RequirementsRequest,
    RequirementsResponse,
)
from .orchestrator import GenerationError, Orchestrator

router = APIRouter(prefix="/api/generate", tags=["generation"])


def get_orchestrator(llm: LLMProvider = Depends(get_llm), kb: KnowledgeBase = Depends(get_kb)) -> Orchestrator:
    return Orchestrator(llm, kb)


def _run(fn, *args):
    try:
        return fn(*args)
    except GenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:  # z. B. fehlender API-Key
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Das Sprachmodell konnte nicht erreicht werden ({type(e).__name__}). "
            "Bitte API-Key und Guthaben pruefen.",
        )


@router.post("/epics", response_model=EpicsResponse)
def epics(req: EpicsRequest, orch: Orchestrator = Depends(get_orchestrator)):
    items, sources = _run(orch.epics, req)
    return EpicsResponse(epics=items, sources=sources)


@router.post("/requirements", response_model=RequirementsResponse)
def requirements(req: RequirementsRequest, orch: Orchestrator = Depends(get_orchestrator)):
    items, sources = _run(orch.requirements, req)
    return RequirementsResponse(requirements=items, sources=sources)


@router.post("/criteria", response_model=CriteriaResponse)
def criteria(req: CriteriaRequest, orch: Orchestrator = Depends(get_orchestrator)):
    items, sources = _run(orch.criteria, req)
    return CriteriaResponse(criteria=items, sources=sources)
