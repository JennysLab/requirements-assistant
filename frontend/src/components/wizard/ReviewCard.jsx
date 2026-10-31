import { useState } from "react";
import { Check, X, RotateCcw, Pencil } from "lucide-react";
import StatusBadge, { statusRailColor } from "../common/StatusBadge.jsx";
import FieldEditor from "./FieldEditor.jsx";

// Karte fuer Epic oder Anforderung: ansehen, bearbeiten, bestaetigen, verwerfen, neu generieren.
export default function ReviewCard({ item, fields, onChange, onStatus, onRegenerate }) {
  const [edit, setEdit] = useState(false);
  return (
    <div className={`rounded-md border border-border border-l-4 bg-surface p-4 ${statusRailColor[item.status]} ${item.status === "verworfen" ? "opacity-60" : ""}`}>
      <div className="mb-2 flex items-center justify-between">
        <span className="font-mono text-xs text-muted">{item.id}</span>
        <StatusBadge status={item.status} />
      </div>
      {edit ? (
        <div className="space-y-3">
          {fields.map((f) => <FieldEditor key={f.key} field={f} value={item[f.key]} onChange={(v) => onChange({ [f.key]: v })} />)}
        </div>
      ) : (
        <div className="space-y-1">
          <h3 className="font-medium">{item.title}</h3>
          {fields.filter((f) => f.key !== "title").map((f) => (
            <p key={f.key} className="text-sm text-muted"><span className="font-medium text-ink">{f.label}: </span>{item[f.key]}</p>
          ))}
        </div>
      )}
      <div className="mt-3 flex gap-1">
        <button title="Bearbeiten" aria-label="Bearbeiten" onClick={() => setEdit(!edit)} className="rounded-sm p-1.5 text-muted hover:bg-paper"><Pencil size={16} /></button>
        <button title="Neu generieren" aria-label="Neu generieren" onClick={onRegenerate} className="rounded-sm p-1.5 text-muted hover:bg-paper"><RotateCcw size={16} /></button>
        <button title="Bestätigen" aria-label="Bestätigen" onClick={() => onStatus("bestaetigt")} className="rounded-sm p-1.5 text-status-accepted hover:bg-status-acceptedsoft"><Check size={16} /></button>
        <button title="Verwerfen" aria-label="Verwerfen" onClick={() => onStatus("verworfen")} className="rounded-sm p-1.5 text-status-rework hover:bg-status-reworksoft"><X size={16} /></button>
      </div>
    </div>
  );
}
