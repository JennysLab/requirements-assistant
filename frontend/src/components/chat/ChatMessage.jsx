export default function ChatMessage({ message }) {
  const user = message.role === "user";
  return (
    <div className={`flex ${user ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[80%] whitespace-pre-wrap rounded-md px-3 py-2 text-sm ${user ? "bg-accent text-white" : message.isError ? "bg-status-reworksoft text-status-rework" : "bg-surface border border-border"}`}>
        {message.text}
        {message.attachments?.length > 0 && <div className="mt-1 text-xs opacity-80">Anhänge: {message.attachments.join(", ")}</div>}
        {message.sources?.length > 0 && (
          <details className="mt-2 border-t border-border pt-2 text-xs text-muted">
            <summary className="cursor-pointer">Quellen ({message.sources.length})</summary>
            <ul className="mt-1 space-y-1">
              {message.sources.map((s) => (
                <li key={s.n}><span className="font-mono">[{s.n}]</span> {s.document}, Abschnitt {s.chunk_index + 1}: {s.text.slice(0, 140)}…</li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </div>
  );
}
