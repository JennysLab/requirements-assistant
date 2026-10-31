import PageHeader from "../components/common/PageHeader.jsx";
import PlaceholderNotice from "../components/common/PlaceholderNotice.jsx";
import { useSettings } from "../context/SettingsContext.jsx";
import { TEMPLATES } from "../templates/templates.js";

export default function SettingsPage() {
  const { templateId, setTemplateId, user } = useSettings();
  return (
    <>
      <PageHeader title="Einstellungen" />
      <div className="space-y-6">
        <section className="rounded-md border border-border bg-surface p-4">
          <h2 className="mb-2 font-semibold">Benutzer</h2>
          <p className="text-sm text-muted">{user.name}</p>
          <div className="mt-2"><PlaceholderNotice>Anmeldung ist ein Platzhalter.</PlaceholderNotice></div>
        </section>
        <section className="rounded-md border border-border bg-surface p-4">
          <h2 className="mb-2 font-semibold">Template für neue Durchläufe</h2>
          {Object.values(TEMPLATES).map((t) => (
            <label key={t.id} className="mb-2 flex items-start gap-2 text-sm">
              <input type="radio" name="tpl" checked={templateId === t.id} onChange={() => setTemplateId(t.id)} className="mt-1" />
              <span><b>{t.name}</b><br /><span className="text-muted">{t.description}</span></span>
            </label>
          ))}
          <PlaceholderNotice>Später definiert ein Agent im Hintergrund Template und Antwortstil.</PlaceholderNotice>
        </section>
      </div>
    </>
  );
}
