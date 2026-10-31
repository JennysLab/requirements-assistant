import { useWizard } from "../../context/WizardContext.jsx";
const STEPS = ["Eingabe", "Epics", "Anforderungen", "Kriterien", "Zusammenfassung"];
export default function WizardProgress() {
  const { step, maxStep, goTo } = useWizard();
  return (
    <ol className="mb-6 flex flex-wrap gap-2">
      {STEPS.map((l, i) => {
        const n = i + 1;
        const cls = n === step ? "bg-accent text-white" : n <= maxStep ? "bg-accent-soft text-accent" : "bg-surface text-muted border border-border";
        return (
          <li key={l}>
            <button disabled={n > maxStep} onClick={() => goTo(n)} className={`rounded-sm px-3 py-1 text-xs font-medium ${cls}`}>
              <span className="font-mono">{n}</span> {l}
            </button>
          </li>
        );
      })}
    </ol>
  );
}
