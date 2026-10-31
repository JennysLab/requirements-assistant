"""Test ohne echtes Sprachmodell: ein Fake liefert feste Antworten."""
from fastapi.testclient import TestClient

from app.generation.router import get_llm
from app.knowledge.router import get_kb
from app.knowledge.store import KnowledgeBase
from app.main import app


class FakeLLM:
    def __init__(self):
        self.calls = []
        self.bad_first = False

    def generate_text(self, messages, system=None):
        return "x"

    def generate_structured(self, messages, tool_name, tool_description, input_schema, system=None):
        self.calls.append((tool_name, messages[0]["content"], input_schema))
        if tool_name == "return_epics":
            if self.bad_first and len(self.calls) == 1:
                return {"epics": [{"title": "nur Titel"}]}
            return {"epics": [{"title": "E1", "description": "d"}]}
        if tool_name == "return_requirements":
            return {"requirements": [{"title": "R1", "description": "Als A moechte ich B, damit C.", "priority": "Hoch"}]}
        return {"criteria": ["Es geht.", "Fehler werden gemeldet."]}


TEMPLATE = {
    "name": "t",
    "epic": [{"key": "title", "label": "Titel"}, {"key": "description", "label": "Beschreibung", "type": "textarea"}],
    "requirement": [
        {"key": "title", "label": "Titel"},
        {"key": "description", "label": "Beschreibung", "type": "textarea", "hint": "Als <Rolle> moechte ich <Ziel>, damit <Nutzen>."},
        {"key": "priority", "label": "Prioritaet", "type": "select", "options": ["Hoch", "Mittel", "Niedrig"]},
    ],
}


def client(fake, kb=None):
    app.dependency_overrides[get_llm] = lambda: fake
    app.dependency_overrides[get_kb] = lambda: kb
    return TestClient(app)


def test_epics_and_schema_from_template():
    fake = FakeLLM()
    r = client(fake).post("/api/generate/epics", json={"input": "Nutzerverwaltung", "template": TEMPLATE})
    assert r.status_code == 200, r.text
    assert r.json()["epics"][0]["title"] == "E1"
    assert "Nutzerverwaltung" in fake.calls[0][1]


def test_requirements_schema_has_enum_and_hint_in_prompt():
    fake = FakeLLM()
    r = client(fake).post("/api/generate/requirements",
                          json={"input": "x", "template": TEMPLATE, "epic": {"title": "E", "description": "d"}})
    assert r.status_code == 200, r.text
    schema = fake.calls[0][2]
    assert schema["properties"]["requirements"]["items"]["properties"]["priority"]["enum"] == ["Hoch", "Mittel", "Niedrig"]
    assert "Als <Rolle>" in fake.calls[0][1]


def test_criteria():
    r = client(FakeLLM()).post("/api/generate/criteria",
                               json={"input": "x", "template": TEMPLATE, "epic": {"title": "E"}, "requirement": {"title": "R"}})
    assert r.json()["criteria"] == ["Es geht.", "Fehler werden gemeldet."]


def test_retry_on_invalid_answer():
    fake = FakeLLM(); fake.bad_first = True
    r = client(fake).post("/api/generate/epics", json={"input": "x", "template": TEMPLATE})
    assert r.status_code == 200 and len(fake.calls) == 2


def test_invalid_template_rejected():
    r = client(FakeLLM()).post("/api/generate/epics", json={"input": "x", "template": {"epic": [], "requirement": []}})
    assert r.status_code == 422


def test_knowledge_is_used_in_prompt_and_returned(tmp_path):
    from test_knowledge import FakeEmbed
    kb = KnowledgeBase(path=tmp_path, embedding_function=FakeEmbed())
    kb.add_document("atlas.txt", "Nutzer Rolle Konto Nutzer Rolle")
    fake = FakeLLM()
    r = client(fake, kb).post("/api/generate/epics", json={"input": "Nutzer und Rolle", "template": TEMPLATE})
    assert r.status_code == 200, r.text
    assert "Wissen aus der Wissensbasis" in fake.calls[0][1] and "atlas.txt" in fake.calls[0][1]
    assert r.json()["sources"][0]["document"] == "atlas.txt"
    # abgeschaltet: kein Wissensabschnitt
    fake2 = FakeLLM()
    r2 = client(fake2, kb).post("/api/generate/epics", json={"input": "Nutzer", "template": TEMPLATE, "use_knowledge": False})
    assert "Wissen aus der Wissensbasis" not in fake2.calls[0][1] and r2.json()["sources"] == []
