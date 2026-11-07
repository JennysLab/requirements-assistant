import PageHeader from "../components/common/PageHeader.jsx";
import PlaceholderNotice from "../components/common/PlaceholderNotice.jsx";
import { useSettings } from "../context/SettingsContext.jsx";

export default function SettingsPage() {
  const { user } = useSettings();
  return (
    <>
      <PageHeader title="Einstellungen" />
      <div className="space-y-6">
        <section className="rounded-md border border-border bg-surface p-4">
          <h2 className="mb-2 font-semibold">Benutzer</h2>
          <p className="text-sm text-muted">{user.name}</p>
          <div className="mt-2"><PlaceholderNotice>Anmeldung ist ein Platzhalter.</PlaceholderNotice></div>
        </section>
      </div>
    </>
  );
}