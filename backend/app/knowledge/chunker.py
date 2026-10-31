"""
Teilt einen Text in Stuecke (Chunks) von ungefaehr einer halben Seite.
Es wird an Absaetzen geschnitten; ein kleiner Teil des vorigen Stuecks
wird wiederholt (Ueberlappung), damit Zusammenhaenge nicht abreissen.
"""
from typing import List


def chunk_text(text: str, size: int = 900, overlap: int = 150) -> List[str]:
    paragraphs = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n") if p.strip()]
    # Sehr lange Absaetze werden hart in Teile der Groesse `size` zerlegt.
    pieces: List[str] = []
    for p in paragraphs:
        while len(p) > size:
            cut = p.rfind(" ", 0, size)
            cut = cut if cut > size // 2 else size
            pieces.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            pieces.append(p)

    chunks: List[str] = []
    current = ""
    for piece in pieces:
        if current and len(current) + len(piece) + 2 > size:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = (tail + "\n\n" + piece).strip() if tail else piece
        else:
            current = (current + "\n\n" + piece).strip() if current else piece
    if current:
        chunks.append(current)
    return chunks
