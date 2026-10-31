// Baut aus den bestaetigten Wizard-Ergebnissen die Nutzlast fuer den Jira-Push.
// Titel wird zur Zusammenfassung. Alle uebrigen Template-Felder ausser der
// Prioritaet (bewusst weggelassen) kommen in die Beschreibung. Die
// Akzeptanzkriterien haengt das Backend als Liste an die Beschreibung an.
import { getTemplate } from "../templates/templates.js";

const describe = (item, fields) =>
  fields
    .filter((f) => f.key !== "title" && f.key !== "priority" && (item[f.key] || "").trim())
    .map((f) => (f.key === "description" ? item[f.key].trim() : `*${f.label}:* ${item[f.key].trim()}`))
    .join("\n\n");

export function buildJiraPayload({ templateId, epics, requirements, criteria }) {
  const t = getTemplate(templateId);
  return {
    epics: epics
      .filter((e) => e.status === "bestaetigt")
      .map((e) => ({
        title: e.title,
        description: describe(e, t.epic),
        requirements: requirements
          .filter((r) => r.status === "bestaetigt" && r.epicId === e.id)
          .map((r) => ({
            title: r.title,
            description: describe(r, t.requirement),
            criteria: criteria.filter((c) => c.status === "bestaetigt" && c.requirementId === r.id).map((c) => c.text),
          })),
      })),
  };
}
