import { createContext, useContext, useState, useCallback } from "react";
import { useSettings } from "./SettingsContext.jsx";
import * as gen from "../services/generationService.js";
import { readFiles } from "../lib/readFiles.js";

// Zustand des Wizards: 1 Eingabe, 2 Epics, 3 Anforderungen, 4 Kriterien, 5 Zusammenfassung.
// Der Zustand liegt im Browser; das Backend bekommt bei jedem Schritt mit, was es braucht.
// Das Template wird beim Start des Durchlaufs festgehalten.
const Ctx = createContext(null);
const initial = { step: 1, maxStep: 1, input: "", attachments: [], epics: [], requirements: [], criteria: [], templateId: null,
  useKnowledge: true, sources: { epics: [], requirements: [], criteria: [] } };

export function WizardProvider({ children }) {
  const { templateId: settingsTemplate } = useSettings();
  const [s, setS] = useState(initial);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const goTo = (step) => setS((o) => (step <= o.maxStep ? { ...o, step } : o));
  const advance = (step, extra = {}) => setS((o) => ({ ...o, ...extra, step, maxStep: Math.max(o.maxStep, step) }));
  const reset = () => { setS(initial); setError(""); };

  const run = useCallback(async (fn) => {
    setLoading(true); setError("");
    try { await fn(); } catch (e) { setError(e.message || "Fehler bei der Generierung."); }
    finally { setLoading(false); }
  }, []);

  // Quellen ohne Dubletten sammeln (gleiches Dokument und gleicher Abschnitt nur einmal).
  const mergeSources = (old, add) => {
    const seen = new Set(old.map((x) => `${x.document}#${x.chunk_index}`));
    return [...old, ...add.filter((x) => !seen.has(`${x.document}#${x.chunk_index}`))];
  };

  const startGeneration = (input, files, useKnowledge = true) => run(async () => {
    const tpl = settingsTemplate;
    const attachments = await readFiles(files || []);
    const { items: epics, sources } = await gen.generateEpics(input, attachments, tpl, useKnowledge);
    // Neuer Durchlauf: alles Spaetere verwerfen, Template festhalten.
    advance(2, {
      input, attachments, epics, requirements: [], criteria: [], templateId: tpl, useKnowledge,
      sources: { epics: sources, requirements: [], criteria: [] },
    });
  });

  const toRequirements = () => run(async () => {
    const confirmed = s.epics.filter((e) => e.status === "bestaetigt");
    const have = new Set(s.requirements.map((r) => r.epicId));
    let reqs = [...s.requirements];
    let src = s.sources.requirements;
    for (const e of confirmed) {
      if (have.has(e.id)) continue;
      const r = await gen.generateRequirements(e, s.templateId, s.input, s.attachments, s.useKnowledge);
      reqs = reqs.concat(r.items);
      src = mergeSources(src, r.sources);
    }
    advance(3, { requirements: reqs, sources: { ...s.sources, requirements: src } });
  });

  const toCriteria = () => run(async () => {
    const okEpics = s.epics.filter((e) => e.status === "bestaetigt");
    const confirmed = s.requirements.filter((r) => r.status === "bestaetigt" && okEpics.some((e) => e.id === r.epicId));
    const have = new Set(s.criteria.map((c) => c.requirementId));
    let crit = [...s.criteria];
    let src = s.sources.criteria;
    for (const r of confirmed) {
      if (have.has(r.id)) continue;
      const epic = okEpics.find((e) => e.id === r.epicId);
      const c = await gen.generateCriteria(r, epic, s.templateId, s.input, s.useKnowledge);
      crit = crit.concat(c.items);
      src = mergeSources(src, c.sources);
    }
    advance(4, { criteria: crit, sources: { ...s.sources, criteria: src } });
  });

  const toSummary = () => advance(5);

  const updateItem = (list, id, p) => setS((o) => ({ ...o, [list]: o[list].map((i) => (i.id === id ? { ...i, ...p } : i)) }));
  const setStatus = (list, id, status) => updateItem(list, id, { status });
  const addItem = (list, item) => setS((o) => ({ ...o, [list]: [...o[list], item] }));

  const regenerate = (list, kind, item) => run(async () => {
    const ctx = {
      templateId: s.templateId, input: s.input, attachments: s.attachments, useKnowledge: s.useKnowledge,
      epic: kind === "requirement" ? s.epics.find((e) => e.id === item.epicId) : null,
    };
    updateItem(list, item.id, await gen.regenerateItem(kind, item, ctx));
  });

  return (
    <Ctx.Provider value={{ ...s, loading, error, goTo, reset, startGeneration, toRequirements, toCriteria, toSummary, updateItem, setStatus, addItem, regenerate }}>
      {children}
    </Ctx.Provider>
  );
}
export const useWizard = () => useContext(Ctx);
