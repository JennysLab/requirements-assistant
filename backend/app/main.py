"""
Einstiegspunkt der FastAPI-App. Startet man lokal mit:
    uvicorn app.main:app --reload --port 8000

Im Container liefert dieselbe App zusaetzlich das fertig gebaute Frontend aus
(Umgebungsvariable FRONTEND_DIST). Dann gibt es nur eine Adresse fuer
Oberflaeche und API, und es sind keine CORS-Freigaben noetig.
"""
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import get_settings
from app.generation.router import router as generation_router
from app.jira.router import router as jira_router
from app.knowledge.router import router as knowledge_router
from app.routers import chat, requirements

settings = get_settings()

app = FastAPI(
    title="KI-Assistenz Anforderungsmanagement - Backend",
    description="Vermittelt zwischen dem React-Frontend und dem LLM-Provider.",
    version="0.1.0",
)

# CORS: nur explizit erlaubte Frontend-Ursprünge duerfen Anfragen stellen
# (per Default nur der lokale Vite-Dev-Server). Ueber CORS_ALLOW_ORIGINS
# in der .env erweiterbar, z. B. um eine spaetere Deployment-URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(requirements.router)
app.include_router(generation_router)
app.include_router(knowledge_router)
app.include_router(jira_router)


@app.get("/api/health")
def health():
    # Fuer Gesundheitspruefungen (z. B. durch den Container oder den Load Balancer).
    return {"status": "ok", "service": "requirements-assistant-backend"}


# Frontend ausliefern, falls ein gebautes Frontend vorhanden ist (Container).
# Lokal ist FRONTEND_DIST nicht gesetzt, dann laeuft das Frontend ueber den
# Vite-Dev-Server und diese Routen entfallen.
_dist = Path(os.environ.get("FRONTEND_DIST", "")) if os.environ.get("FRONTEND_DIST") else None

if _dist and (_dist / "index.html").is_file():
    _dist = _dist.resolve()

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str):
        # Unbekannte API-Adressen sollen ein echter 404 sein, nicht die Startseite.
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        # Eine vorhandene Datei (Skripte, Bilder, Styles) direkt ausliefern.
        # Der Pfad wird geprueft, damit nichts ausserhalb des Frontend-Ordners
        # gelesen werden kann.
        candidate = (_dist / full_path).resolve()
        if full_path and candidate.is_file() and _dist in candidate.parents:
            return FileResponse(candidate)
        # Alles andere (z. B. /anforderungen) ist eine Seite des Frontends:
        # die Startdatei ausliefern, das Routing uebernimmt der Browser.
        return FileResponse(_dist / "index.html")
else:
    @app.get("/")
    def health_check():
        # Dient nur zum schnellen manuellen Check im Browser, ob der Server laeuft.
        return {"status": "ok", "service": "requirements-assistant-backend"}
