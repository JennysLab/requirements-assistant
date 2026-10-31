import { Check, X } from "lucide-react";
import { statusRailColor } from "../common/StatusBadge.jsx";

export default function CriterionRow({ item, onChange, onStatus }) {
  return (
    <div className={`flex items-center gap-2 rounded-md border border-border border-l-4 bg-surface px-3 py-2 ${statusRailColor[item.status]} ${item.status === "verworfen" ? "opacity-60" : ""}`}>
      <span className="font-mono text-xs text-muted">{item.id}</span>
      <input value={item.text} onChange={(e) => onChange({ text: e.target.value })} className="flex-1 bg-transparent text-sm outline-none" aria-label="Akzeptanzkriterium" />
      <button aria-label="Bestätigen" onClick={() => onStatus("bestaetigt")} className="rounded-sm p-1 text-status-accepted hover:bg-status-acceptedsoft"><Check size={16} /></button>
      <button aria-label="Verwerfen" onClick={() => onStatus("verworfen")} className="rounded-sm p-1 text-status-rework hover:bg-status-reworksoft"><X size={16} /></button>
    </div>
  );
}
