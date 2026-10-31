export default function CounterPills({ items }) {
  const c = (s) => items.filter((i) => i.status === s).length;
  return (
    <div className="mb-4 flex gap-2 text-xs">
      <span className="rounded-sm bg-surface px-2 py-1 border border-border">Gesamt <b className="font-mono">{items.length}</b></span>
      <span className="rounded-sm bg-status-acceptedsoft px-2 py-1 text-status-accepted">Bestätigt <b className="font-mono">{c("bestaetigt")}</b></span>
      <span className="rounded-sm bg-status-reworksoft px-2 py-1 text-status-rework">Verworfen <b className="font-mono">{c("verworfen")}</b></span>
    </div>
  );
}
