import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { getJson, postFile, deleteJson } from "../lib/apiClient.js";

// Wissensbasis (Modul M1): Dokumente liegen im Backend (Chroma).
// Dieser Context holt die Liste, laedt hoch und loescht.
const Ctx = createContext(null);
const RESULT = { neu: "hinzugefügt", aktualisiert: "aktualisiert (neue Version)", unveraendert: "unverändert, nichts zu tun" };

export function KnowledgeBaseProvider({ children }) {
  const [docs, setDocs] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const refresh = useCallback(async () => {
    try { setDocs((await getJson("/api/knowledge/documents")).documents); setError(""); }
    catch (e) { setError(e.message); }
  }, []);
  useEffect(() => { refresh(); }, [refresh]);

  const addFiles = async (files) => {
    setBusy(true); setError(""); setNotice("");
    const messages = [];
    for (const f of Array.from(files)) {
      try {
        const r = await postFile("/api/knowledge/documents", f);
        messages.push(`${f.name}: ${RESULT[r.result] || r.result} (${r.chunks} Abschnitte)`);
      } catch (e) { setError(`${f.name}: ${e.message}`); }
    }
    setNotice(messages.join(" · "));
    await refresh();
    setBusy(false);
  };

  const removeDoc = async (id) => {
    setError(""); setNotice("");
    try { await deleteJson(`/api/knowledge/documents/${id}`); await refresh(); }
    catch (e) { setError(e.message); }
  };

  return <Ctx.Provider value={{ docs, busy, error, notice, addFiles, removeDoc }}>{children}</Ctx.Provider>;
}
export const useKnowledgeBase = () => useContext(Ctx);
