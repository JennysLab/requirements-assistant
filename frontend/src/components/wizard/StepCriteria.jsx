import CriterionRow from "./CriterionRow.jsx";
import CounterPills from "./CounterPills.jsx";
import SourcesNote from "./SourcesNote.jsx";
import WizardFooter from "./WizardFooter.jsx";
import { useWizard } from "../../context/WizardContext.jsx";
import { getTemplate } from "../../templates/templates.js";

export default function StepCriteria() {
  const w = useWizard();
  const tpl = getTemplate(w.templateId);
  const reqs = w.requirements.filter((r) => r.status === "bestaetigt");
  return (
    <div>
      <SourcesNote sources={w.sources.criteria} enabled={w.useKnowledge} />
      <CounterPills items={w.criteria} />
      {reqs.map((r) => (
        <section key={r.id} className="mb-6">
          <h2 className="mb-1 text-sm font-semibold"><span className="font-mono text-muted">{r.id}</span> {r.title}</h2>
          <p className="mb-2 text-xs text-muted">{tpl.criteriaLabel}</p>
          <div className="space-y-2">
            {w.criteria.filter((c) => c.requirementId === r.id).map((c) => (
              <CriterionRow key={c.id} item={c} onChange={(p) => w.updateItem("criteria", c.id, p)} onStatus={(s) => w.setStatus("criteria", c.id, s)} />
            ))}
          </div>
        </section>
      ))}
      <WizardFooter onNext={w.toSummary} nextLabel="Zusammenfassung" />
    </div>
  );
}
