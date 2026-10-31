/**
 * GENERIERUNGSSERVICE
 * Ruft das Backend (/api/generate/...) auf. Das Template wird als Daten
 * mitgeschickt, das Backend baut daraus Schema und Prompt und holt, wenn
 * gewuenscht, passendes Wissen aus der Wissensbasis.
 * Jede Funktion liefert { items, sources }: die Ergebnisse und die genutzten
 * Wissensquellen. Ohne Backend: in .env  VITE_USE_MOCK=true  setzen.
 */
import { postJson } from "../lib/apiClient.js";
import { getTemplate } from "../templates/templates.js";
import * as mock from "./mockGeneration.js";

const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";
let counter = 0;
const uid = (p) => `${p}-${String(++counter).padStart(3, "0")}`;

const tplPayload = (id) => {
  const t = getTemplate(id);
  return { name: t.name, epic: t.epic, requirement: t.requirement };
};
// Nur die Template-Felder eines Eintrags ans Backend schicken.
const pick = (item, fields) => Object.fromEntries(fields.map((f) => [f.key, item[f.key] || ""]));

export async function generateEpics(input, attachments, templateId, useKnowledge = true) {
  if (USE_MOCK) return { items: await mock.generateEpics(), sources: [] };
  const res = await postJson("/api/generate/epics", {
    input, attachments, template: tplPayload(templateId), use_knowledge: useKnowledge,
  });
  return { items: res.epics.map((e) => ({ id: uid("EP"), ...e, status: "entwurf" })), sources: res.sources || [] };
}

export async function generateRequirements(epic, templateId, input, attachments = [], useKnowledge = true) {
  if (USE_MOCK) return { items: await mock.generateRequirements(epic, templateId), sources: [] };
  const t = getTemplate(templateId);
  const res = await postJson("/api/generate/requirements", {
    input, attachments, template: tplPayload(templateId), epic: pick(epic, t.epic), use_knowledge: useKnowledge,
  });
  return {
    items: res.requirements.map((r) => ({ id: uid("RQ"), epicId: epic.id, ...r, status: "entwurf" })),
    sources: res.sources || [],
  };
}

export async function generateCriteria(requirement, epic, templateId, input, useKnowledge = true) {
  if (USE_MOCK) return { items: await mock.generateCriteria(requirement), sources: [] };
  const t = getTemplate(templateId);
  const res = await postJson("/api/generate/criteria", {
    input, template: tplPayload(templateId), epic: pick(epic, t.epic),
    requirement: pick(requirement, t.requirement), use_knowledge: useKnowledge,
  });
  return {
    items: res.criteria.map((text) => ({ id: uid("AK"), requirementId: requirement.id, text, status: "entwurf" })),
    sources: res.sources || [],
  };
}

// "Neu generieren": das Backend ueberarbeitet den bisherigen Entwurf.
export async function regenerateItem(kind, item, ctx) {
  if (USE_MOCK) return mock.regenerateItem(kind, item);
  const t = getTemplate(ctx.templateId);
  const base = { input: ctx.input, attachments: ctx.attachments, template: tplPayload(ctx.templateId), use_knowledge: ctx.useKnowledge };
  if (kind === "epic") {
    const res = await postJson("/api/generate/epics", { ...base, revise: pick(item, t.epic) });
    return { ...item, ...res.epics[0], status: "entwurf" };
  }
  const res = await postJson("/api/generate/requirements", { ...base, epic: pick(ctx.epic, t.epic), revise: pick(item, t.requirement) });
  return { ...item, ...res.requirements[0], status: "entwurf" };
}
