import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage.jsx";
import ChatInput from "./ChatInput.jsx";
import { useChat } from "../../context/ChatContext.jsx";
import { SUGGESTIONS } from "../../mock/mockData.js";

export default function ChatWindow() {
  const { messages, sending, send } = useChat();
  const end = useRef(null);
  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);
  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex-1 space-y-3 overflow-y-auto rounded-md border border-border bg-paper p-4">
        {messages.map((m) => <ChatMessage key={m.id} message={m} />)}
        {sending && <div className="text-sm text-muted">Buddy schreibt…</div>}
        <div ref={end} />
      </div>
      {messages.length <= 1 && (
        <div className="flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => <button key={s} onClick={() => send(s)} className="rounded-sm border border-border bg-surface px-3 py-1 text-xs hover:bg-accent-soft">{s}</button>)}
        </div>
      )}
      <ChatInput rows={2} allowAttach={false} disabled={sending} placeholder="Frage stellen…" onSubmit={(t, f) => send(t, f.map((x) => x.name))} />
    </div>
  );
}
