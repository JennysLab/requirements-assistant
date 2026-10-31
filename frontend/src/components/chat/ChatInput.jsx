import { useRef, useState } from "react";
import { Paperclip, Send, X } from "lucide-react";
import Button from "../common/Button.jsx";

// Eingabefeld mit Anhaengen. Reicht Text und Dateinamen an onSubmit weiter.
export default function ChatInput({ onSubmit, disabled, placeholder, rows = 3, submitLabel = "Senden", allowAttach = true }) {
  const [text, setText] = useState("");
  const [files, setFiles] = useState([]);
  const ref = useRef(null);
  const submit = () => {
    if (!text.trim() || disabled) return;
    onSubmit(text.trim(), files);
    setText(""); setFiles([]);
  };
  return (
    <div className="rounded-md border border-border bg-surface p-3">
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows={rows} placeholder={placeholder}
        onKeyDown={(e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submit(); }}
        className="w-full resize-none bg-transparent text-sm outline-none" />
      {files.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-2">
          {files.map((f, i) => (
            <span key={i} className="inline-flex items-center gap-1 rounded-sm bg-accent-soft px-2 py-1 text-xs text-accent">
              {f.name}
              <button aria-label="Anhang entfernen" onClick={() => setFiles(files.filter((_, j) => j !== i))}><X size={12} /></button>
            </span>
          ))}
        </div>
      )}
      <div className="flex items-center justify-between">
        {allowAttach ? (
          <button type="button" onClick={() => ref.current.click()} className="inline-flex items-center gap-1 text-sm text-muted hover:text-ink">
            <Paperclip size={16} /> Anhang
          </button>
        ) : <span />}
        <input ref={ref} type="file" multiple hidden onChange={(e) => setFiles([...files, ...Array.from(e.target.files)])} />
        <Button onClick={submit} disabled={disabled || !text.trim()}><Send size={16} /> {submitLabel}</Button>
      </div>
    </div>
  );
}
