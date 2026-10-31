"""
Einstiegspunkt der FastAPI-App. Startet man lokal mit:
    uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def health_check():
    # Dient nur zum schnellen manuellen Check im Browser, ob der Server laeuft.
    return {"status": "ok", "service": "requirements-assistant-backend"}
