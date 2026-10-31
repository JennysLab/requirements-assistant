/**
 * Zentraler Helfer fuer Aufrufe an das FastAPI-Backend. Basis-URL aus
 * VITE_API_BASE_URL, sonst http://localhost:8000.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch (networkError) {
    throw new Error(
      `Backend nicht erreichbar unter ${API_BASE_URL}. Läuft "uvicorn app.main:app --port 8000"?`
    );
  }
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    let detail = text;
    try { const j = JSON.parse(text); if (typeof j.detail === "string") detail = j.detail; } catch (e) { /* kein JSON */ }
    throw new Error(`Backend-Fehler (${response.status}): ${detail || response.statusText}`);
  }
  return response.json();
}

export const getJson = (path) => request(path);
export const deleteJson = (path) => request(path, { method: "DELETE" });
export const postJson = (path, body) =>
  request(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
// Datei-Upload (multipart). Der Browser setzt den Content-Type selbst.
export const postFile = (path, file) => {
  const form = new FormData();
  form.append("file", file);
  return request(path, { method: "POST", body: form });
};
