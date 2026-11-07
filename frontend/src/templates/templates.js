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
    description: "User Story im Jira-Stil: Titel, Beschreibung, Priorität.",
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
      { key: "priority", label: "Priorität", type: "select", options: ["Hoch", "Mittel", "Niedrig"] },
    ],
    criteriaLabel: "Akzeptanzkriterien (Checkliste)",
  },
  satzschablone: {
    id: "satzschablone",
    name: "Satzschablone",
    description: "Formale Anforderung nach Satzschablone mit MoSCoW-Priorität.",
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
                hint: "Satzschablone: [Bedingung,] das System muss/soll/wird [<wem> die Möglichkeit bieten | fähig sein] <Objekt mit Ergänzung> <Prozesswort>. Die Teile in eckigen Klammern nur, wenn nötig. Beispiel: Wenn der Kunde angemeldet ist, muss das System dem Kunden die Möglichkeit bieten, Rechnungen als PDF herunterzuladen.",
      },
      { key: "rationale", label: "Begründung", type: "textarea" },
      { key: "priority", label: "Priorität", type: "select", options: ["Muss", "Soll", "Kann"] },
    ],
    criteriaLabel: "Akzeptanzkriterien",
  },
};

export const DEFAULT_TEMPLATE_ID = "jira-standard";
export const getTemplate = (id) => TEMPLATES[id] || TEMPLATES[DEFAULT_TEMPLATE_ID];
