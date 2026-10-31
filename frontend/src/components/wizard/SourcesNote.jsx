import { BookOpen } from "lucide-react";

// Zeigt, welche Stellen der Wissensbasis in diesem Schritt als Hintergrund genutzt wurden.
export default function SourcesNote({ sources, enabled }) {
  if (!enabled) return <p className="mb-4 text-xs text-muted">Wissensbasis wurde für diesen Durchlauf nicht genutzt.</p>;
  if (!sources || sources.length === 0)
    return <p className="mb-4 text-xs text-muted">Keine passenden Stellen in der Wissensbasis gefunden.</p>;
  return (
    <details className="mb-4 rounded-md border border-border bg-surface px-3 py-2 text-xs">
      <summary className="flex cursor-pointer items-center gap-2 text-muted">
        <BookOpen size={14} /> Genutzte Wissensquellen ({sources.length})
      </summary>
      <ul className="mt-2 space-y-2">
        {sources.map((s, i) => (
          <li key={i}>
            <span className="font-medium">{s.document}</span>
            <span className="text-muted"> · Abschnitt {s.chunk_index + 1}</span>
            <p className="text-muted">{s.text.slice(0, 200)}…</p>
          </li>
        ))}
      </ul>
    </details>
  );
}
