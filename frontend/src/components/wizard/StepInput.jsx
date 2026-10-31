import { useState } from "react";
import ChatInput from "../chat/ChatInput.jsx";
import { useWizard } from "../../context/WizardContext.jsx";
import { useSettings } from "../../context/SettingsContext.jsx";
import { getTemplate } from "../../templates/templates.js";

export default function StepInput() {
  const { startGeneration, input, loading } = useWizard();
  const { templateId } = useSettings();
  const [useKnowledge, setUseKnowledge] = useState(true);
  return (
    <div className="space-y-4">
      <p className="text-sm text-muted">Beschreibe grob, was gebaut werden soll. Anhänge sind möglich. Template: <b>{getTemplate(templateId).name}</b></p>
      {input && <p className="rounded-md border border-border bg-surface p-3 text-sm">Letzte Eingabe: {input}</p>}
      <ChatInput rows={5} disabled={loading} submitLabel="Epics generieren" placeholder="z. B. Wir brauchen eine Nutzerverwaltung mit Rollen…" onSubmit={(t, f) => startGeneration(t, f, useKnowledge)} />
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={useKnowledge} onChange={(e) => setUseKnowledge(e.target.checked)} />
        Wissensbasis berücksichtigen (passende Stellen aus deinen Dokumenten fließen ein)
      </label>
      
    </div>
  );
}
