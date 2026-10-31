import { NavLink, Outlet, Link } from "react-router-dom";
import { Home, Settings, User } from "lucide-react";

const link = ({ isActive }) => `rounded-sm px-3 py-1.5 text-sm ${isActive ? "bg-white/15 text-white" : "text-sidebarmuted hover:text-white"}`;

export default function AppLayout() {
  return (
    <div className="min-h-screen">
      <header className="flex items-center gap-4 bg-sidebar px-6 py-3">
        <Link to="/" aria-label="Startseite" className="text-white"><Home size={18} /></Link>
        <nav className="flex flex-1 gap-1">
          <NavLink to="/anforderungen" className={link}>Anforderungen generieren</NavLink>
          <NavLink to="/buddy" className={link}>Virtual Buddy</NavLink>
          <NavLink to="/einstellungen" className={link}><Settings size={14} className="mr-1 inline" />Einstellungen</NavLink>
        </nav>
        <span className="flex items-center gap-2 text-sm text-sidebarmuted"><User size={16} /> Nicht angemeldet</span>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-8"><Outlet /></main>
    </div>
  );
}
