"""
Buddy-Chat mit Wissensbasis (RAG): Vor jedem Modellaufruf werden die
passendsten Textstellen gesucht und in den Prompt gelegt. Das Modell
antwortet daraus und nennt die Quellen.
"""
from pathlib import Path
from typing import Any, Dict, List, Tuple

from app.llm.base import LLMProvider

from .store import KnowledgeBase

PROMPT = Path(__file__).parent / "prompts" / "buddy.md"


def _query_from(messages: List[Dict[str, str]]) -> str:
    # Die letzten zwei Nutzerfragen, damit kurze Rueckfragen ("und dann?") Kontext haben.
    user = [m["content"] for m in messages if m["role"] == "user"]
    return " ".join(user[-2:])


def answer(llm: LLMProvider, kb: KnowledgeBase, messages: List[Dict[str, str]], k: int = 4) -> Tuple[str, List[Dict[str, Any]]]:
    hits = kb.search(_query_from(messages), k)
    sources = [
        {"n": i + 1, "document": h["document"], "version": h["version"],
         "chunk_index": h["chunk_index"], "text": h["text"]}
        for i, h in enumerate(hits)
    ]
    if sources:
        context = "\n\n".join(f"[{s['n']}] {s['document']} (Abschnitt {s['chunk_index'] + 1})\n{s['text']}" for s in sources)
    else:
        context = "(Die Wissensbasis enthält keine Dokumente oder keine passenden Stellen.)"
    system = PROMPT.read_text(encoding="utf-8").replace("{{context}}", context)
    reply = llm.generate_text(messages, system=system)
    return reply, sources
