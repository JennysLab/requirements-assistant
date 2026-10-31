import { createContext, useContext, useState } from "react";
import { postJson } from "../lib/apiClient.js";
import { WELCOME } from "../mock/mockData.js";

// Chat des Virtual Buddy. Nutzt das Backend (/api/knowledge/chat): Antworten
// kommen aus den Dokumenten der Wissensbasis, mit Quellenangabe.
const Ctx = createContext(null);

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState(WELCOME);
  const [sending, setSending] = useState(false);

  const send = async (text, attachments = []) => {
    const user = { id: `u${Date.now()}`, role: "user", text, attachments };
    const history = [...messages, user];
    setMessages(history);
    setSending(true);
    try {
      const res = await postJson("/api/knowledge/chat", { messages: history.map(({ role, text }) => ({ role, content: text })) });
      setMessages((m) => [...m, { id: `a${Date.now()}`, role: "assistant", text: res.reply, sources: res.sources || [] }]);
    } catch (e) {
      setMessages((m) => [...m, { id: `e${Date.now()}`, role: "assistant", text: e.message, isError: true }]);
    } finally { setSending(false); }
  };
  return <Ctx.Provider value={{ messages, sending, send }}>{children}</Ctx.Provider>;
}
export const useChat = () => useContext(Ctx);
