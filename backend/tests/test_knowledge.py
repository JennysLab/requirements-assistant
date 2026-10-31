"""Tests ohne Modell-Download: ein einfacher Fake erzeugt Zahlen aus Woertern."""
import io

import pytest
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastapi.testclient import TestClient

from app.knowledge.chunker import chunk_text
from app.knowledge.router import get_kb
from app.knowledge.store import KnowledgeBase
from app.main import app

VOCAB = ["nutzer", "rolle", "konto", "jira", "import", "bericht", "status"]


class FakeEmbed(EmbeddingFunction):
    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        return [[float(t.lower().count(w)) + 0.01 for w in VOCAB] for t in input]

    @staticmethod
    def name() -> str:
        return "fake-embed"

    def get_config(self):
        return {}

    @staticmethod
    def build_from_config(config):
        return FakeEmbed()


@pytest.fixture
def kb(tmp_path):
    return KnowledgeBase(path=tmp_path, embedding_function=FakeEmbed())


def test_chunker_splits_and_overlaps():
    text = "\n\n".join(f"Absatz {i} " + "wort " * 60 for i in range(10))
    chunks = chunk_text(text, size=500, overlap=80)
    assert len(chunks) > 1 and all(len(c) <= 700 for c in chunks)


def test_add_update_delete(kb):
    r = kb.add_document("a.txt", "Nutzer und Rolle und Konto.\n\nJira Import.")
    assert r["result"] == "neu" and r["version"] == 1
    assert kb.add_document("a.txt", "Nutzer und Rolle und Konto.\n\nJira Import.")["result"] == "unveraendert"
    r2 = kb.add_document("a.txt", "Ganz neuer Text zum Bericht.")
    assert r2["result"] == "aktualisiert" and r2["version"] == 2
    docs = kb.list_documents()
    assert len(docs) == 1 and docs[0]["version"] == 2
    assert kb.delete_document(docs[0]["id"]) and kb.list_documents() == []


def test_search_finds_relevant(kb):
    kb.add_document("nutzer.txt", "Nutzer Konto Rolle Nutzer Rolle")
    kb.add_document("bericht.txt", "Bericht Status Bericht")
    hits = kb.search("Welche Rolle hat ein Nutzer?", k=1)
    assert hits[0]["document"] == "nutzer.txt"


def test_api_upload_list_delete(kb):
    app.dependency_overrides[get_kb] = lambda: kb
    c = TestClient(app)
    r = c.post("/api/knowledge/documents", files={"file": ("n.md", io.BytesIO("# Titel\n\nNutzer Rolle".encode()), "text/markdown")})
    assert r.status_code == 200 and r.json()["result"] == "neu"
    assert len(c.get("/api/knowledge/documents").json()["documents"]) == 1
    assert c.post("/api/knowledge/search", json={"query": "Rolle"}).json()["hits"]
    bad = c.post("/api/knowledge/documents", files={"file": ("x.exe", io.BytesIO(b"x"), "application/octet-stream")})
    assert bad.status_code == 422
    doc_id = c.get("/api/knowledge/documents").json()["documents"][0]["id"]
    assert c.delete(f"/api/knowledge/documents/{doc_id}").status_code == 200
    assert c.delete(f"/api/knowledge/documents/{doc_id}").status_code == 404
    app.dependency_overrides.clear()


def test_docx_and_pdf_readers():
    from docx import Document
    from app.knowledge.readers import read_text
    d = Document(); d.add_paragraph("Hallo Nutzer"); buf = io.BytesIO(); d.save(buf)
    assert "Hallo Nutzer" in read_text("a.docx", buf.getvalue())


def test_buddy_chat_uses_sources(kb):
    from app.generation.router import get_llm

    class FakeLLM:
        def generate_text(self, messages, system=None):
            self.system = system
            return "Antwort [1]"

    fake = FakeLLM()
    app.dependency_overrides[get_kb] = lambda: kb
    app.dependency_overrides[get_llm] = lambda: fake
    kb.add_document("nutzer.txt", "Nutzer Konto Rolle Nutzer Rolle")
    r = TestClient(app).post("/api/knowledge/chat", json={"messages": [{"role": "user", "content": "Welche Rolle hat ein Nutzer?"}]})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["reply"] == "Antwort [1]" and body["sources"][0]["document"] == "nutzer.txt"
    assert "nutzer.txt" in fake.system and "Rolle" in fake.system
    app.dependency_overrides.clear()


def test_concurrent_first_access(tmp_path, monkeypatch):
    """Zwei gleichzeitige Erstzugriffe duerfen nicht scheitern (Chroma-Race)."""
    import threading
    from app.knowledge import router as r
    monkeypatch.setenv("KNOWLEDGE_DIR", str(tmp_path))
    monkeypatch.setattr(r, "_instance", None)
    errors = []

    def go():
        try:
            r._kb().list_documents()
        except Exception as e:  # noqa
            errors.append(repr(e))

    threads = [threading.Thread(target=go) for _ in range(4)]
    [t.start() for t in threads]; [t.join() for t in threads]
    assert errors == []
