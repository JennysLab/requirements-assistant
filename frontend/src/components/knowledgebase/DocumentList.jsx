import { useRef } from "react";
import { FileText, Trash2, Upload, Loader2 } from "lucide-react";
import { useKnowledgeBase } from "../../context/KnowledgeBaseContext.jsx";

export default function DocumentList() {
  const { docs, busy, error, notice, addFiles, removeDoc } = useKnowledgeBase();
  const ref = useRef(null);
  return (
    <div className="space-y-3">
      <button disabled={busy} onClick={() => ref.current.click()} onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); addFiles(e.dataTransfer.files); }}
        className="flex w-full flex-col items-center gap-1 rounded-md border border-dashed border-border bg-surface p-4 text-sm text-muted hover:bg-accent-soft disabled:opacity-60">
        {busy ? <Loader2 size={18} className="animate-spin" /> : <Upload size={18} />}
        {busy ? "Wird verarbeitet… (beim ersten Mal dauert es länger)" : "Dokumente hochladen oder hierher ziehen"}
        <span className="text-xs">txt, md, docx, pdf</span>
      </button>
      <input ref={ref} type="file" multiple hidden accept=".txt,.md,.csv,.json,.docx,.pdf"
        onChange={(e) => { addFiles(e.target.files); e.target.value = ""; }} />
      {error && <p role="alert" className="rounded-md bg-status-reworksoft px-3 py-2 text-xs text-status-rework">{error}</p>}
      {notice && <p className="rounded-md bg-status-acceptedsoft px-3 py-2 text-xs text-status-accepted">{notice}</p>}
      {docs.length === 0 && !error && <p className="text-sm text-muted">Noch keine Dokumente in der Wissensbasis.</p>}
      <ul className="space-y-2">
        {docs.map((d) => (
          <li key={d.id} className="flex items-center gap-3 rounded-md border border-border bg-surface px-3 py-2 text-sm">
            <FileText size={16} className="shrink-0 text-muted" />
            <span className="min-w-0 flex-1 truncate" title={d.name}>{d.name}</span>
            <span className="whitespace-nowrap font-mono text-xs text-muted">v{d.version} · {d.chunks} Abschn.</span>
            <button aria-label={`${d.name} entfernen`} onClick={() => removeDoc(d.id)} className="text-muted hover:text-status-rework"><Trash2 size={16} /></button>
          </li>
        ))}
      </ul>
    </div>
  );
}
