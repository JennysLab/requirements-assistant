import { createContext, useContext, useState } from "react";
import { DEFAULT_TEMPLATE_ID } from "../templates/templates.js";

// Einstellungen und Platzhalter fuer den angemeldeten Nutzer.
// TODO: Echte Anmeldung ergaenzen, sobald das Konzept steht.
const Ctx = createContext(null);

export function SettingsProvider({ children }) {
  const [templateId, setTemplateId] = useState(DEFAULT_TEMPLATE_ID);
  const [user] = useState({ name: "Nicht angemeldet", role: "Platzhalter" });
  return <Ctx.Provider value={{ templateId, setTemplateId, user }}>{children}</Ctx.Provider>;
}
export const useSettings = () => useContext(Ctx);
