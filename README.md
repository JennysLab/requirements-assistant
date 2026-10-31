# Requirements Assistant

Prototyp zur Masterarbeit **„KI-Assistenz im Requirements Engineering"**
(Design Science Research, Wirtschaftsinformatik).

Der Prototyp unterstützt dabei, aus einer groben Idee Epics, Anforderungen und
Akzeptanzkriterien zu entwerfen und nach Jira zu übertragen. Jedes Ergebnis ist
ein Entwurf, den ein Mensch prüft, bearbeitet und bestätigt (Human-in-the-Loop).

## Bestandteile

| Ordner | Inhalt |
|---|---|
| `frontend/` | React-Anwendung (Wizard, Virtual Buddy, Einstellungen) |
| `backend/` | FastAPI-Anwendung (Generierung, Wissensbasis, Jira-Übergabe) |
| `docs/` | Dokumentation und Architektur |

## Architektur in Kürze

Ports und Adapter: Die Fachlogik kennt nur Schnittstellen (LLM-Anbieter,
Wissensbasis, Ticketsystem). Konkrete Werkzeuge sind austauschbare Adapter.
Das Backend ist zustandslos, Anforderungen werden nicht dauerhaft gespeichert
(keine Primärspeicherung), Jira bleibt das führende System.

## Lokal starten

Backend:

```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # danach Schlüssel in .env eintragen
uvicorn app.main:app --reload --port 8000
```

Frontend (zweites Terminal):

```
cd frontend
npm install
npm run dev
```

Anwendung: http://localhost:5173 · API-Dokumentation: http://localhost:8000/docs

## Sicherheit

API-Schlüssel und Tokens stehen ausschließlich in der lokalen Datei
`backend/.env`. Diese Datei ist per `.gitignore` ausgeschlossen und darf nie
eingecheckt werden.

## Tests

```
cd backend
source .venv/bin/activate
pytest
```

## Stand

Lokal lauffähig. Offen: Qualitätsprüfung, Deployment auf AWS, Zugriffsschutz,
Evaluation.
