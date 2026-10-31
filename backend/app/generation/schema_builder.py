"""
Baut aus den Feldern eines Templates (a) das JSON-Schema, das die Antwort des
Sprachmodells erfuellen muss, und (b) den Feldabschnitt fuer den Prompt.
"""
from typing import Any, Dict, List

from .models import FieldDef


def item_schema(fields: List[FieldDef]) -> Dict[str, Any]:
    props: Dict[str, Any] = {}
    for f in fields:
        desc = f.label + (f" - {f.hint}" if f.hint else "")
        prop: Dict[str, Any] = {"type": "string", "description": desc}
        if f.type == "select" and f.options:
            prop["enum"] = list(f.options)
        props[f.key] = prop
    return {"type": "object", "properties": props, "required": [f.key for f in fields]}


def list_schema(list_key: str, fields: List[FieldDef]) -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {list_key: {"type": "array", "items": item_schema(fields)}},
        "required": [list_key],
    }


def criteria_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "criteria": {
                "type": "array",
                "items": {"type": "string", "description": "Ein pruefbares Akzeptanzkriterium"},
            }
        },
        "required": ["criteria"],
    }


def fields_prompt(fields: List[FieldDef]) -> str:
    lines = []
    for f in fields:
        line = f"- {f.key} ({f.label})"
        if f.hint:
            line += f": {f.hint}"
        if f.type == "select" and f.options:
            line += " Erlaubte Werte: " + ", ".join(f.options) + "."
        lines.append(line)
    return "\n".join(lines)
