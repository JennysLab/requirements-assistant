"""
IssueTracker: der "Port" fuer das Ticketsystem (Ports and Adapters).
Der Rest der Anwendung kennt nur diesen Vertrag, nicht Jira. Ein anderes
Werkzeug (Azure DevOps, GitLab ...) bedeutet: einen neuen Adapter schreiben.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IssueRef:
    key: str
    url: str


class IssueTracker(ABC):
    @abstractmethod
    def describe(self) -> Dict[str, Any]:
        """Prueft Zugang und Projekt und liefert eine Kurzbeschreibung des Ziels."""

    @abstractmethod
    def create_epic(self, title: str, description: str) -> IssueRef:
        ...

    @abstractmethod
    def create_story(self, title: str, description: str, epic_key: Optional[str]) -> IssueRef:
        ...
