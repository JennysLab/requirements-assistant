"""
Orchestrator: steuert die Generierung Schritt fuer Schritt.

Pro Wizard-Schritt (Epics, Anforderungen, Kriterien) macht er immer dasselbe:
  1. Prompt aus einer Textdatei (prompts/) laden und mit den Daten fuellen
  2. Ausgabeschema aus dem Template bauen
  3. Sprachmodell ueber den Port LLMProvider aufrufen
  4. Antwort pruefen (bei Fehler einmal wiederholen)
  5. Aufruf protokollieren (fuer die Evaluation, Kapitel 7)

Der Orchestrator kennt keinen konkreten Anbieter, nur den Port LLMProvider.
Er speichert keine Nutzerdaten ausser dem lokalen Protokoll. Der Zustand
des Wizards liegt im Frontend und wird bei jeder Anfrage mitgeschickt.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.knowledge.store import KnowledgeBase
from app.llm.base import LLMProvider

from . import schema_builder as sb
from .models import (
    Attachment,
    CriteriaRequest,
    EpicsRequest,
    FieldDef,
    RequirementsRequest,
)

HERE = Path(__file__).parent
MAX_ATTACHMENT_CHARS = 20000


class GenerationError(Exception):
    pass


class Orchestrator:
    def __init__(self, llm: LLMProvider, kb: Optional[KnowledgeBase] = None, prompt_dir: Path = HERE / "prompts", log_dir: Optional[Path] = HERE / "logs"):
        self._llm = llm
        self._kb = kb
        self._prompt_dir = prompt_dir
        self._log_dir = log_dir

    # ---- Oeffentliche Schritte -------------------------------------------

    def epics(self, req: EpicsRequest) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        fields = req.template.epic
        knowledge, sources = self._knowledge(req.input[:600], req.use_knowledge)
        revise = self._revise_block(req.revise, "Epic")
        prompt = self._prompt(
            "epics",
            count=str(1 if req.revise else req.count),
            input=req.input,
            attachments=self._attachments(req.attachments),
            fields=sb.fields_prompt(fields),
            revise=revise,
            knowledge=knowledge,
        )
        items = self._call("epics", prompt, "return_epics", "Gibt Epics zurueck.",
                          sb.list_schema("epics", fields), "epics", fields, req.model_dump(), sources)
        return items, sources

    def requirements(self, req: RequirementsRequest) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        fields = req.template.requirement
        knowledge, sources = self._knowledge(self._item_text(req.epic) + " " + req.input[:300], req.use_knowledge)
        revise = self._revise_block(req.revise, "Anforderung")
        prompt = self._prompt(
            "requirements",
            count=str(1 if req.revise else req.count),
            input=req.input,
            attachments=self._attachments(req.attachments),
            epic=self._item_text(req.epic),
            fields=sb.fields_prompt(fields),
            revise=revise,
            knowledge=knowledge,
        )
        items = self._call("requirements", prompt, "return_requirements", "Gibt Anforderungen zurueck.",
                          sb.list_schema("requirements", fields), "requirements", fields, req.model_dump(), sources)
        return items, sources

    def criteria(self, req: CriteriaRequest) -> Tuple[List[str], List[Dict[str, Any]]]:
        knowledge, sources = self._knowledge(self._item_text(req.requirement), req.use_knowledge)
        prompt = self._prompt(
            "criteria",
            count=str(req.count),
            input=req.input,
            epic=self._item_text(req.epic),
            requirement=self._item_text(req.requirement),
            knowledge=knowledge,
        )
        result = self._call("criteria", prompt, "return_criteria", "Gibt Akzeptanzkriterien zurueck.",
                            sb.criteria_schema(), "criteria", None, req.model_dump(), sources)
        return result, sources

    # ---- Hilfsfunktionen -------------------------------------------------

    def _knowledge(self, query: str, use: bool, k: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """Sucht passende Stellen in der Wissensbasis und baut den Promptabschnitt."""
        if not use or self._kb is None or not query.strip():
            return "", []
        hits = self._kb.search(query, k)
        if not hits:
            return "", []
        sources = [
            {"n": i + 1, "document": h["document"], "version": h["version"],
             "chunk_index": h["chunk_index"], "text": h["text"]}
            for i, h in enumerate(hits)
        ]
        body = "\n\n".join(f"[{s['n']}] {s['document']}\n{s['text']}" for s in sources)
        block = (
            "# Wissen aus der Wissensbasis\n"
            "Nutze diese Textstellen als Hintergrund. Widersprich ihnen nicht und halte Begriffe und Rollen konsistent. "
            "Verwende nur, was zur Aufgabe passt, und ignoriere unpassende Stellen.\n\n" + body
        )
        return block, sources

    def _prompt(self, name: str, **values: str) -> str:
        text = (self._prompt_dir / f"{name}.md").read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        return text.strip()

    def _system(self) -> str:
        return (self._prompt_dir / "system.md").read_text(encoding="utf-8").strip()

    @staticmethod
    def _item_text(item: Dict[str, str]) -> str:
        return "\n".join(f"{k}: {v}" for k, v in item.items())

    @staticmethod
    def _revise_block(item: Optional[Dict[str, str]], kind: str) -> str:
        if not item:
            return ""
        return (
            f"# Ueberarbeitung\nUeberarbeite diesen bisherigen Entwurf ({kind}). Behalte die Aussage, "
            f"verbessere Klarheit und Vollstaendigkeit. Liefere genau einen Eintrag.\n"
            f"{Orchestrator._item_text(item)}"
        )

    @staticmethod
    def _attachments(attachments: List[Attachment]) -> str:
        parts, used = [], 0
        for a in attachments:
            if not a.text.strip():
                continue
            chunk = a.text[: max(0, MAX_ATTACHMENT_CHARS - used)]
            if not chunk:
                break
            used += len(chunk)
            parts.append(f"Anhang {a.name}:\n{chunk}")
        return "\n\n".join(parts)

    @staticmethod
    def _check(result: Dict[str, Any], key: str, fields: Optional[List[FieldDef]]) -> List[Any]:
        items = result.get(key)
        if not isinstance(items, list) or not items:
            raise GenerationError(f"Antwort enthaelt keine Liste '{key}'.")
        for item in items:
            if fields is None:
                if not isinstance(item, str) or not item.strip():
                    raise GenerationError("Ein Kriterium ist leer oder kein Text.")
                continue
            if not isinstance(item, dict):
                raise GenerationError("Ein Eintrag hat nicht die erwartete Form.")
            for f in fields:
                value = item.get(f.key)
                if not isinstance(value, str) or not value.strip():
                    raise GenerationError(f"Feld '{f.key}' fehlt oder ist leer.")
                if f.type == "select" and f.options and value not in f.options:
                    raise GenerationError(f"Feld '{f.key}' hat einen unerlaubten Wert.")
        return items

    def _call(self, step, prompt, tool_name, tool_desc, schema, key, fields, request_dump, sources=None):
        started = time.time()
        error = ""
        for attempt in (1, 2):  # ein zweiter Versuch bei ungueltiger Antwort
            raw = self._llm.generate_structured(
                messages=[{"role": "user", "content": prompt}],
                tool_name=tool_name,
                tool_description=tool_desc,
                input_schema=schema,
                system=self._system(),
            )
            try:
                items = self._check(raw, key, fields)
                self._log(step, request_dump, prompt, raw, attempt, started, "", sources)
                return items
            except GenerationError as e:
                error = str(e)
        self._log(step, request_dump, prompt, raw, 2, started, error, sources)
        raise GenerationError(f"Das Modell lieferte keine gueltige Antwort: {error}")

    def _log(self, step, request_dump, prompt, raw, attempts, started, error, sources=None):
        if not self._log_dir:
            return
        try:
            self._log_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            entry = {
                "step": step,
                "duration_s": round(time.time() - started, 2),
                "attempts": attempts,
                "error": error,
                "request": request_dump,
                "knowledge_sources": sources or [],
                "prompt": prompt,
                "result": raw,
            }
            (self._log_dir / f"{stamp}-{step}.json").write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except OSError:
            pass  # Protokoll ist optional und darf die Generierung nicht stoppen
