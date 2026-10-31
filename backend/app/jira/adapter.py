"""
JiraAdapter: der einzige Ort, der die Jira-Cloud-REST-API kennt (API v2,
Beschreibungen als Jira-Wiki-Text). Zugangsdaten kommen aus der .env.

Vorgangstypen werden aus dem Projekt gelesen, nicht fest verdrahtet:
  Epic  = Typ "Epic" (oder der Typ auf Hierarchie-Ebene 1)
  Story = Typ "Story", sonst "Task"
Die Story wird dem Epic ueber das Feld "parent" zugeordnet.
"""
from typing import Any, Dict, List, Optional

import httpx

from .port import IssueRef, IssueTracker


class JiraError(Exception):
    pass


FOOTER = "_Entwurf erzeugt mit der KI-Assistenz und vom Menschen bestätigt._"


def render_description(description: str, criteria: Optional[List[str]] = None) -> str:
    parts: List[str] = []
    if description.strip():
        parts.append(description.strip())
    if criteria:
        parts.append("h3. Akzeptanzkriterien\n" + "\n".join(f"* {c.strip()}" for c in criteria if c.strip()))
    parts.append(FOOTER)
    return "\n\n".join(parts)


class JiraAdapter(IssueTracker):
    def __init__(self, base_url: str, email: str, api_token: str, project_key: str,
                 transport: Optional[httpx.BaseTransport] = None):
        self._base = base_url.rstrip("/")
        self._project = project_key.strip().upper()
        self._client = httpx.Client(
            base_url=self._base,
            auth=(email, api_token),
            headers={"Accept": "application/json"},
            timeout=30,
            transport=transport,
        )
        self._types: Optional[Dict[str, Dict[str, str]]] = None

    # ---- Port ------------------------------------------------------------

    def describe(self) -> Dict[str, Any]:
        types = self._issue_types()
        return {
            "base_url": self._base,
            "project_key": self._project,
            "epic_type": types["epic"]["name"],
            "story_type": types["story"]["name"],
        }

    def create_epic(self, title: str, description: str) -> IssueRef:
        return self._create(title, description, self._issue_types()["epic"]["id"], None)

    def create_story(self, title: str, description: str, epic_key: Optional[str]) -> IssueRef:
        return self._create(title, description, self._issue_types()["story"]["id"], epic_key)

    # ---- intern ----------------------------------------------------------

    def _issue_types(self) -> Dict[str, Dict[str, str]]:
        if self._types is None:
            data = self._request("GET", f"/rest/api/2/project/{self._project}")
            items = [t for t in data.get("issueTypes", []) if not t.get("subtask")]
            epic = next((t for t in items if t["name"].lower() == "epic"), None) or \
                next((t for t in items if t.get("hierarchyLevel") == 1), None)
            story = next((t for t in items if t["name"].lower() == "story"), None) or \
                next((t for t in items if t["name"].lower() == "task"), None)
            if not epic:
                raise JiraError("Im Jira-Projekt gibt es keinen Vorgangstyp 'Epic'.")
            if not story:
                raise JiraError("Im Jira-Projekt gibt es weder 'Story' noch 'Task' als Vorgangstyp.")
            self._types = {"epic": epic, "story": story}
        return self._types

    def _create(self, title: str, description: str, type_id: str, parent_key: Optional[str]) -> IssueRef:
        fields: Dict[str, Any] = {
            "project": {"key": self._project},
            "summary": " ".join(title.split())[:250] or "(ohne Titel)",
            "description": description,
            "issuetype": {"id": type_id},
        }
        if parent_key:
            fields["parent"] = {"key": parent_key}
        data = self._request("POST", "/rest/api/2/issue", {"fields": fields})
        key = data["key"]
        return IssueRef(key=key, url=f"{self._base}/browse/{key}")

    def _request(self, method: str, path: str, body: Optional[dict] = None) -> Dict[str, Any]:
        try:
            r = self._client.request(method, path, json=body)
        except httpx.HTTPError as e:
            raise JiraError(f"Jira ist nicht erreichbar ({type(e).__name__}). Adresse und Internet prüfen.")
        if r.status_code in (200, 201):
            return r.json()
        if r.status_code == 401:
            raise JiraError("Anmeldung bei Jira fehlgeschlagen. E-Mail-Adresse und API-Token prüfen.")
        if r.status_code == 403:
            raise JiraError("Jira verweigert den Zugriff. Fehlt das Recht, Vorgänge in diesem Projekt anzulegen?")
        if r.status_code == 404:
            raise JiraError(f"Projekt '{self._project}' nicht gefunden. Projekt-Kürzel und Jira-Adresse prüfen.")
        detail = ""
        try:
            j = r.json()
            detail = "; ".join(j.get("errorMessages", []) + [f"{k}: {v}" for k, v in j.get("errors", {}).items()])
        except ValueError:
            pass
        raise JiraError(f"Jira meldet einen Fehler ({r.status_code}): {detail or r.text[:200]}")
