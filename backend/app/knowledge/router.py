"""
API-Adressen der Wissensbasis (Modul M1):
  GET    /api/knowledge/documents        Liste
  POST   /api/knowledge/documents        Datei hochladen
  DELETE /api/knowledge/documents/{id}   Dokument loeschen
  POST   /api/knowledge/search           Suche (zum Pruefen der Treffer)
"""
import threading
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from .readers import ReadError, read_text
from .store import KnowledgeBase

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])
MAX_BYTES = 10 * 1024 * 1024


_lock = threading.Lock()
_instance: Optional[KnowledgeBase] = None


def _kb() -> KnowledgeBase:
    # Die Sperre ist noetig: Das Frontend schickt beim Start zwei Anfragen
    # fast gleichzeitig. Chroma darf aber nur einmal initialisiert werden.
    global _instance
    with _lock:
        if _instance is None:
            _instance = KnowledgeBase()
        return _instance


def get_kb() -> KnowledgeBase:
    return _kb()


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    k: int = Field(default=4, ge=1, le=10)


@router.get("/documents")
def list_documents(kb: KnowledgeBase = Depends(get_kb)):
    return {"documents": kb.list_documents()}


@router.post("/documents")
async def upload_document(file: UploadFile = File(...), kb: KnowledgeBase = Depends(get_kb)):
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Datei ist groesser als 10 MB.")
    try:
        text = read_text(file.filename or "", data)
    except ReadError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        return kb.add_document(file.filename, text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speichern in der Wissensbasis fehlgeschlagen ({type(e).__name__}).",
        )


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str, kb: KnowledgeBase = Depends(get_kb)):
    if not kb.delete_document(doc_id):
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden.")
    return {"deleted": doc_id}


@router.post("/search")
def search(req: SearchRequest, kb: KnowledgeBase = Depends(get_kb)):
    return {"hits": kb.search(req.query, req.k)}


# ---- Buddy-Chat mit Wissensbasis -------------------------------------------
from app.llm.factory import get_llm  # der eine Ort, der den Anbieter kennt
from app.llm.base import LLMProvider

from . import buddy


class ChatMsg(BaseModel):
    role: str
    content: str


class BuddyChatRequest(BaseModel):
    messages: List[ChatMsg] = Field(..., min_length=1)


@router.post("/chat")
def buddy_chat(req: BuddyChatRequest, kb: KnowledgeBase = Depends(get_kb), llm: LLMProvider = Depends(get_llm)):
    try:
        reply, sources = buddy.answer(llm, kb, [m.model_dump() for m in req.messages])
    except ValueError as e:  # z. B. fehlender API-Key
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Das Sprachmodell konnte nicht erreicht werden ({type(e).__name__}). Bitte API-Key und Guthaben pruefen.",
        )
    return {"reply": reply, "sources": sources}
