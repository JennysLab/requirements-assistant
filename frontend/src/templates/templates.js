/**
 * TEMPLATES
 * Ein Template ist reine Daten: Es beschreibt, welche Felder ein Epic, eine
 * Anforderung und ein Akzeptanzkriterium haben. Die Oberflaeche rendert die
 * Felder aus dieser Beschreibung. So kann das Template spaeter ausgetauscht
 * werden (z. B. durch einen Agenten im Hintergrund), ohne die UI zu aendern.
 *
 * Feldtypen: "text" (einzeilig), "textarea" (mehrzeilig), "select" (Auswahl)
 */
export const TEMPLATES = {
  "jira-standard": {
    id: "jira-standard",
    name: "Jira-Standard",
    description: "User Story im Jira-Stil: Titel und Beschreibung.",
    epic: [
      { key: "title", label: "Titel", type: "text" },
      { key: "description", label: "Beschreibung", type: "textarea" },
    ],
    requirement: [
      { key: "title", label: "Titel", type: "text" },
      {
        key: "description",
        label: "Beschreibung",
        type: "textarea",
        hint: "Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.",
      },
    ],
    criteriaLabel: "Akzeptanzkriterien (Checkliste)",
  },
  satzschablone: {
    id: "satzschablone",
    name: "Satzschablone",
    description: "Formale Anforderung nach Satzschablone mit Begründung.",
    epic: [
      { key: "title", label: "Titel", type: "text" },
      { key: "description", label: "Beschreibung", type: "textarea" },
    ],
    requirement: [
      { key: "title", label: "Titel", type: "text" },
      {
        key: "description",
        label: "Anforderung",
        type: "textarea",
                hint: "Satzschablone nach Pohl und Rupp: [Bedingung,] das System muss/soll/wird, danach entweder nichts, oder [wem] die Möglichkeit bieten, oder fähig sein, dann <Objekt mit Ergänzung> und am Ende das <Prozesswort>. Die Bedingung steht nur, wenn sie nötig ist. Beispiele: Wenn der Kunde angemeldet ist, muss das System dem Kunden die Möglichkeit bieten, Rechnungen als PDF herunterzuladen. Das System muss fähig sein, 100 Anfragen pro Sekunde zu verarbeiten. Das System muss Rechnungen archivieren.",
      },
      { key: "rationale", label: "Begründung", type: "textarea" },
    ],
    criteriaLabel: "Akzeptanzkriterien",
  },
};

export const DEFAULT_TEMPLATE_ID = "satzschablone";
export const getTemplate = (id) => TEMPLATES[id] || TEMPLATES[DEFAULT_TEMPLATE_ID];