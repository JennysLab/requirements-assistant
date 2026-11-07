import { Download } from "lucide-react";
import Button from "../common/Button.jsx";
import JiraPushPanel from "./JiraPushPanel.jsx";
import WizardFooter from "./WizardFooter.jsx";
import { useWizard } from "../../context/WizardContext.jsx";

export default function StepSummary() {
  const w = useWizard();
  const epics = w.epics.filter((e) => e.status === "bestaetigt");
  const reqs = w.requirements.filter((r) => r.status === "bestaetigt");
  const crit = w.criteria.filter((c) => c.status === "bestaetigt");
  const exportJson = () => {
    const data = { template: w.templateId, epics: epics.map((e) => ({ ...e, requirements: reqs.filter((r) => r.epicId === e.id).map((r) => ({ ...r, criteria: crit.filter((c) => c.requirementId === r.id) })) })) };
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
    a.download = "anforderungen.json"; a.click();
  };
  return (
    <div className="space-y-4">
      <p className="text-sm">Bestätigt: <b className="font-mono">{epics.length}</b> Epics, <b className="font-mono">{reqs.length}</b> Anforderungen, <b className="font-mono">{crit.length}</b> Kriterien.</p>
      {epics.map((e) => (
        <div key={e.id} className="rounded-md border border-border bg-surface p-4">
          <h3 className="font-medium"><span className="font-mono text-xs text-muted">{e.id}</span> {e.title}</h3>
          {reqs.filter((r) => r.epicId === e.id).map((r) => (
            <div key={r.id} className="mt-2 pl-3 text-sm">
                            <div><span className="font-mono text-xs text-muted">{r.id}</span> {r.title}</div>
              <ul className="ml-4 list-disc text-muted">{crit.filter((c) => c.requirementId === r.id).map((c) => <li key={c.id}>{c.text}</li>)}</ul>
            </div>
          ))}
        </div>
      ))}
      <div className="flex gap-3">
        <Button variant="secondary" onClick={exportJson}><Download size={16} /> JSON exportieren</Button>
      </div>
      <JiraPushPanel />
      <WizardFooter onNext={w.reset} nextLabel="Neu starten" />
    </div>
  );
}
