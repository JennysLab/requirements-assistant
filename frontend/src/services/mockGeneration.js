/**
 * GENERATIONSSERVICE (aktuell MOCK)
 * Alle Funktionen liefern Beispieldaten mit kuenstlicher Verzoegerung.
 * TODO(Backend-Anbindung): Die Funktionen durch postJson(...) aus lib/apiClient.js
 * ersetzen, sobald die Wizard-Endpunkte im Backend existieren. Die Signaturen
 * bleiben gleich, die Oberflaeche muss dann nicht geaendert werden.
 */
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
let counter = 0;
const uid = (p) => `${p}-${String(++counter).padStart(3, "0")}`;

const EPICS = [
  { title: "Nutzerverwaltung mit Rollen", description: "Nutzer können angelegt werden und erhalten Rollen, die ihre Rechte steuern." },
  { title: "Import bestehender Anforderungen aus Jira", description: "Vorhandene Epics und Stories werden als Kontext eingelesen." },
  { title: "Benachrichtigungen bei Statusänderungen", description: "Beteiligte werden informiert, wenn sich der Status einer Anforderung ändert." },
];

const REQS = {
  0: [
    { title: "Nutzerkonto anlegen", description: "Als Administrator möchte ich ein Nutzerkonto anlegen, damit neue Kolleginnen und Kollegen arbeiten können.", rationale: "Grundlage für jede Zugriffskontrolle.", priority: ["Hoch", "Muss"] },
    { title: "Rollen zuweisen und entziehen", description: "Als Administrator möchte ich Rollen zuweisen und entziehen, damit Rechte zur Aufgabe passen.", rationale: "Rechte müssen nachvollziehbar steuerbar sein.", priority: ["Mittel", "Soll"] },
  ],
  1: [
    { title: "Bestehende Epics als Kontext einlesen", description: "Als Requirements Engineer möchte ich bestehende Epics einlesen, damit neue Anforderungen dazu passen.", rationale: "Vermeidet Dubletten und Widersprüche.", priority: ["Mittel", "Soll"] },
  ],
  2: [
    { title: "Statusbenachrichtigung senden", description: "Als Beteiligte möchte ich bei Statuswechseln benachrichtigt werden, damit ich rechtzeitig reagieren kann.", rationale: "Transparenz im Review-Prozess.", priority: ["Niedrig", "Kann"] },
  ],
};

const CRITERIA = [
  "Die Funktion ist über die Oberfläche erreichbar.",
  "Fehleingaben werden verständlich gemeldet.",
  "Das Ergebnis ist nach dem Speichern sichtbar.",
];

export async function generateEpics(/* input, attachments, templateId */) {
  await wait(900);
  return EPICS.map((e) => ({ id: uid("EP"), ...e, status: "entwurf" }));
}

export async function generateRequirements(epic, templateId) {
  await wait(800);
  const idx = Math.max(0, EPICS.findIndex((e) => e.title === epic.title));
  const list = REQS[idx] || REQS[0];
  const pi = templateId === "satzschablone" ? 1 : 0;
  return list.map((r) => ({
    id: uid("RQ"), epicId: epic.id, title: r.title, description: r.description,
    rationale: r.rationale, priority: r.priority[pi], status: "entwurf",
  }));
}

export async function generateCriteria(requirement) {
  await wait(700);
  return CRITERIA.map((text) => ({ id: uid("AK"), requirementId: requirement.id, text, status: "entwurf" }));
}

export async function regenerateItem(kind, item) {
  await wait(600);
  return { ...item, status: "entwurf", description: (item.description || "") + " (neu generiert)" };
}
