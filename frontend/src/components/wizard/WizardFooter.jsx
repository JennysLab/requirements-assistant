import { ArrowLeft, ArrowRight } from "lucide-react";
import Button from "../common/Button.jsx";
import { useWizard } from "../../context/WizardContext.jsx";

export default function WizardFooter({ onNext, nextLabel = "Weiter", nextDisabled, hint }) {
  const { step, goTo } = useWizard();
  return (
    <div className="mt-6 flex items-center justify-between border-t border-border pt-4">
      <Button variant="secondary" disabled={step <= 1} onClick={() => goTo(step - 1)}><ArrowLeft size={16} /> Zurück</Button>
      <div className="flex items-center gap-3">
        {hint && <span className="text-xs text-muted">{hint}</span>}
        <Button onClick={onNext} disabled={nextDisabled}>{nextLabel} <ArrowRight size={16} /></Button>
      </div>
    </div>
  );
}
