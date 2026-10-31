import ReviewCard from "./ReviewCard.jsx";
import CounterPills from "./CounterPills.jsx";
import SourcesNote from "./SourcesNote.jsx";
import WizardFooter from "./WizardFooter.jsx";
import { useWizard } from "../../context/WizardContext.jsx";
import { getTemplate } from "../../templates/templates.js";

export default function StepRequirements() {
  const w = useWizard();
  const tpl = getTemplate(w.templateId);
  const epics = w.epics.filter((e) => e.status === "bestaetigt");
  const ok = w.requirements.filter((r) => r.status === "bestaetigt").length;
  return (
    <div>
      <SourcesNote sources={w.sources.requirements} enabled={w.useKnowledge} />
      <CounterPills items={w.requirements} />
      {epics.map((e) => (
        <section key={e.id} className="mb-6">
          <h2 className="mb-2 text-sm font-semibold"><span className="font-mono text-muted">{e.id}</span> {e.title}</h2>
          <div className="space-y-3">
            {w.requirements.filter((r) => r.epicId === e.id).map((r) => (
              <ReviewCard key={r.id} item={r} fields={tpl.requirement}
                onChange={(p) => w.updateItem("requirements", r.id, p)} onStatus={(s) => w.setStatus("requirements", r.id, s)}
                onRegenerate={() => w.regenerate("requirements", "requirement", r)} />
            ))}
          </div>
        </section>
      ))}
      <WizardFooter onNext={w.toCriteria} nextDisabled={ok < 1} hint={ok < 1 ? "Mindestens eine Anforderung bestätigen" : ""} />
    </div>
  );
}
