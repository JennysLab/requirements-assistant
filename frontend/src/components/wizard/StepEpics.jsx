import { useState } from "react";
import { Plus } from "lucide-react";
import Button from "../common/Button.jsx";
import ReviewCard from "./ReviewCard.jsx";
import CounterPills from "./CounterPills.jsx";
import SourcesNote from "./SourcesNote.jsx";
import WizardFooter from "./WizardFooter.jsx";
import { useWizard } from "../../context/WizardContext.jsx";
import { getTemplate } from "../../templates/templates.js";

export default function StepEpics() {
  const w = useWizard();
  const tpl = getTemplate(w.templateId);
  const ok = w.epics.filter((e) => e.status === "bestaetigt").length;
  const [n, setN] = useState(1);
  return (
    <div>
      <SourcesNote sources={w.sources.epics} enabled={w.useKnowledge} />
      <CounterPills items={w.epics} />
      <div className="space-y-3">
        {w.epics.map((e) => (
          <ReviewCard key={e.id} item={e} fields={tpl.epic}
            onChange={(p) => w.updateItem("epics", e.id, p)} onStatus={(s) => w.setStatus("epics", e.id, s)}
            onRegenerate={() => w.regenerate("epics", "epic", e)} />
        ))}
      </div>
      <Button variant="ghost" className="mt-3" onClick={() => { w.addItem("epics", { id: `EP-M${n}`, title: "Neues Epic", description: "", status: "entwurf" }); setN(n + 1); }}>
        <Plus size={16} /> Epic hinzufügen
      </Button>
      <WizardFooter onNext={w.toRequirements} nextDisabled={ok < 1} hint={ok < 1 ? "Mindestens ein Epic bestätigen" : ""} />
    </div>
  );
}
