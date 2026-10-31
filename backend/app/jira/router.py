"""
API-Adressen fuer Jira (Modul M2):
  GET  /api/jira/status   Ist Jira eingerichtet, und stimmt das Projekt?
  POST /api/jira/push     Bestaetigte Epics und Stories in Jira anlegen
Die Router enthalten keine Jira-Details, die stecken im Adapter.
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import Settings, get_settings

from .adapter import JiraAdapter, JiraError, render_description
from .port import IssueTracker

router = APIRouter(prefix="/api/jira", tags=["jira"])


def get_tracker(settings: Settings = Depends(get_settings)) -> Optional[IssueTracker]:
    # Einzige Stelle, die den konkreten Anbieter kennt. None = nicht eingerichtet.
    if not (settings.jira_base_url and settings.jira_email and settings.jira_api_token and settings.jira_project_key):
        return None
    return JiraAdapter(settings.jira_base_url, settings.jira_email, settings.jira_api_token, settings.jira_project_key)


class PushRequirement(BaseModel):
    title: str
    description: str = ""
    criteria: List[str] = []


class PushEpic(BaseModel):
    title: str
    description: str = ""
    requirements: List[PushRequirement] = []


class PushRequest(BaseModel):
    epics: List[PushEpic] = Field(..., min_length=1)


@router.get("/status")
def status(tracker: Optional[IssueTracker] = Depends(get_tracker)) -> Dict[str, Any]:
    if tracker is None:
        return {"configured": False, "error": "Jira ist nicht eingerichtet. In der .env fehlen Einträge (JIRA_...)."}
    try:
        return {"configured": True, "error": "", **tracker.describe()}
    except JiraError as e:
        return {"configured": True, "error": str(e)}


@router.post("/push")
def push(req: PushRequest, tracker: Optional[IssueTracker] = Depends(get_tracker)) -> Dict[str, Any]:
    if tracker is None:
        raise HTTPException(status_code=400, detail="Jira ist nicht eingerichtet.")
    created: List[Dict[str, str]] = []
    try:
        for epic in req.epics:
            e = tracker.create_epic(epic.title, render_description(epic.description))
            created.append({"type": "Epic", "title": epic.title, "key": e.key, "url": e.url})
            for r in epic.requirements:
                s = tracker.create_story(r.title, render_description(r.description, r.criteria), e.key)
                created.append({"type": "Story", "title": r.title, "key": s.key, "url": s.url, "epic": e.key})
    except JiraError as ex:
        # Schon Angelegtes bleibt in Jira. Der Nutzer sieht, was fertig ist und was fehlt.
        return {"created": created, "failed": str(ex)}
    return {"created": created, "failed": None}
