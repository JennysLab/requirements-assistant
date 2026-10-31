import { Link } from "react-router-dom";
import { FileText, MessageCircle } from "lucide-react";
import PageHeader from "../components/common/PageHeader.jsx";

const Tile = ({ to, icon: Icon, title, text }) => (
  <Link to={to} className="block rounded-md border border-border bg-surface p-6 transition hover:border-accent hover:bg-accent-soft">
    <Icon className="mb-3 text-accent" size={28} />
    <h2 className="text-lg font-semibold">{title}</h2>
    <p className="mt-1 text-sm text-muted">{text}</p>
  </Link>
);

export default function LandingPage() {
  return (
    <>
      <PageHeader title="Willkommen" subtitle="Wähle, womit du starten möchtest." />
      <div className="grid gap-4 md:grid-cols-2">
        <Tile to="/anforderungen" icon={FileText} title="Anforderungen generieren" text="Von der groben Idee zu Epics, Anforderungen und Akzeptanzkriterien – Schritt für Schritt." />
        <Tile to="/buddy" icon={MessageCircle} title="Virtual Buddy" text="Fragen zum System stellen und mit der Wissensbasis chatten." />
      </div>
    </>
  );
}
