"""
KnowledgeBase: die EINZIGE Stelle, die Chroma kennt (Modul M1).
Chat und Wizard sprechen nur mit dieser Klasse. Soll spaeter pgvector oder
ein Cloud-Dienst genutzt werden, wird nur der Inhalt dieser Klasse ersetzt.

Aufgaben: Dokument hinzufuegen / aktualisieren, loeschen, auflisten, suchen.
Aktualisierung (A1.4): Zu jedem Dokument wird ein Fingerabdruck (Hash)
gespeichert. Gleiche Datei = unveraendert. Geaenderte Datei mit gleichem
Namen = alte Stuecke werden ersetzt, die Version steigt.
"""
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb

from .chunker import chunk_text

DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data" / "chroma"


class KnowledgeBase:
    def __init__(self, path: Optional[Path] = None, embedding_function: Any = None):
        path = Path(path or os.environ.get("KNOWLEDGE_DIR") or DEFAULT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(path))
        kwargs: Dict[str, Any] = {"name": "wissensbasis"}
        if embedding_function is not None:
            kwargs["embedding_function"] = embedding_function
        self._col = self._client.get_or_create_collection(**kwargs)

    @staticmethod
    def doc_id(name: str) -> str:
        return hashlib.sha1(name.encode("utf-8")).hexdigest()[:12]

    def add_document(self, name: str, text: str) -> Dict[str, Any]:
        doc_id = self.doc_id(name)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing = self._col.get(where={"doc_id": doc_id}, include=["metadatas"], limit=1)
        version = 1
        if existing["ids"]:
            meta = existing["metadatas"][0]
            if meta.get("content_hash") == content_hash:
                return {**self._summary(meta, self._count(doc_id)), "result": "unveraendert"}
            version = int(meta.get("version", 1)) + 1
            self._col.delete(where={"doc_id": doc_id})

        chunks = chunk_text(text)
        uploaded = datetime.now().isoformat(timespec="seconds")
        self._col.add(
            ids=[f"{doc_id}-{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[
                {
                    "doc_id": doc_id,
                    "doc_name": name,
                    "chunk_index": i,
                    "version": version,
                    "content_hash": content_hash,
                    "uploaded_at": uploaded,
                }
                for i in range(len(chunks))
            ],
        )
        meta = {"doc_id": doc_id, "doc_name": name, "version": version, "uploaded_at": uploaded}
        return {**self._summary(meta, len(chunks)), "result": "aktualisiert" if version > 1 else "neu"}

    def delete_document(self, doc_id: str) -> bool:
        if not self._col.get(where={"doc_id": doc_id}, limit=1)["ids"]:
            return False
        self._col.delete(where={"doc_id": doc_id})
        return True

    def list_documents(self) -> List[Dict[str, Any]]:
        data = self._col.get(include=["metadatas"])
        docs: Dict[str, Dict[str, Any]] = {}
        for meta in data["metadatas"]:
            d = docs.setdefault(meta["doc_id"], self._summary(meta, 0))
            d["chunks"] += 1
        return sorted(docs.values(), key=lambda d: d["name"].lower())

    def search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        total = self._col.count()
        if total == 0 or not query.strip():
            return []
        res = self._col.query(query_texts=[query], n_results=min(k, total), include=["documents", "metadatas", "distances"])
        hits = []
        for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            hits.append({
                "doc_id": meta["doc_id"], "document": meta["doc_name"], "version": meta["version"],
                "chunk_index": meta["chunk_index"], "text": text, "distance": round(float(dist), 4),
            })
        return hits

    # ---- intern ----------------------------------------------------------

    def _count(self, doc_id: str) -> int:
        return len(self._col.get(where={"doc_id": doc_id})["ids"])

    @staticmethod
    def _summary(meta: Dict[str, Any], chunks: int) -> Dict[str, Any]:
        return {
            "id": meta["doc_id"], "name": meta["doc_name"], "version": int(meta.get("version", 1)),
            "uploaded_at": meta.get("uploaded_at", ""), "chunks": chunks,
        }
