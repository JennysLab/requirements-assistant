import { useEffect, useState } from "react";
import { Send, Loader2, ExternalLink } from "lucide-react";
import Button from "../common/Button.jsx";
import { getJson, postJson } from "../../lib/apiClient.js";
import { buildJiraPayload } from "../../lib/jiraPayload.js";
import { useWizard } from "../../context/WizardContext.jsx";

// Jira-Push mit Vorschau: erst pruefen, dann bewusst anlegen, danach Links zeigen.
export default function JiraPushPanel() {
  const w = useWizard();
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const payload = buildJiraPayload(w);
  const nEpics = payload.epics.length;
  const nStories = payload.epics.reduce((n, e) => n + e.requirements.length, 0);

  useEffect(() => {
    getJson("/api/jira/status").then(setStatus).catch((e) => setError(e.message));
  }, []);

  const push = async () => {
    setBusy(true); setError("");
    try { setResult(await postJson("/api/jira/push", payload)); }
    catch (e) { setError(e.message); }
    finally { setBusy(false); }
  };

  const ready = status && status.configured && !status.error;
  const done = result && !result.failed;

  return (
    <section className="space-y-3 rounded-md border border-border bg-surface p-4">
      <h3 className="font-medium">An Jira senden</h3>
      {!status && !error && <p className="text-sm text-muted">Prüfe Jira-Zugang…</p>}
      {status && !ready && <p role="alert" className="rounded-md bg-status-reworksoft px-3 py-2 text-sm text-status-rework">{status.error}</p>}
      {ready && (
        <p className="text-sm text-muted">
          Ziel: Projekt <b className="font-mono">{status.project_key}</b> auf {status.base_url}. Epics als „{status.epic_type}“, Anforderungen als „{status.story_type}“,
          Akzeptanzkriterien in der Beschreibung.
        </p>
      )}
      <p className="text-sm">Es werden <b className="font-mono">{nEpics}</b> Epics und <b className="font-mono">{nStories}</b> Stories angelegt.</p>
      {error && <p role="alert" className="rounded-md bg-status-reworksoft px-3 py-2 text-sm text-status-rework">{error}</p>}
      {result && result.failed && <p role="alert" className="rounded-md bg-status-reworksoft px-3 py-2 text-sm text-status-rework">Abgebrochen: {result.failed}. Bereits angelegte Einträge bleiben in Jira.</p>}
      {result && result.created.length > 0 && (
        <ul className="space-y-1 text-sm">
          {result.created.map((c) => (
            <li key={c.key}>
              <a href={c.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-accent hover:underline">
                <span className="font-mono">{c.key}</span> <ExternalLink size={12} />
              </a>{" "}
              <span className="text-muted">{c.type}: {c.title}</span>
            </li>
          ))}
        </ul>
      )}
      {!done && (
        <Button onClick={push} disabled={!ready || busy || nEpics === 0 || (result && result.created.length > 0)}>
          {busy ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />} In Jira anlegen
        </Button>
      )}
      {done && <p className="text-sm text-status-accepted">Fertig. Zum erneuten Senden starte einen neuen Durchlauf, sonst entstehen Dubletten.</p>}
    </section>
  );
}
