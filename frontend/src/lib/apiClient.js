/**
 * Zentraler Helfer fuer Aufrufe an das FastAPI-Backend ("der Bote").
 * Alle Seiten und Contexts sprechen das Backend nur ueber diese Datei an.
 * So steht die Adresse an einer Stelle: Zieht das Backend spaeter in die Cloud
 * um, wird nur VITE_API_BASE_URL (Datei .env des Frontends) geaendert, nicht
 * der Code. Ohne Angabe gilt http://localhost:8000.
 */
// "??" statt "||": Ein leerer Wert ist erlaubt und bedeutet "gleiche Adresse wie die
// Seite selbst". So laeuft das Frontend im Container ohne feste Backend-Adresse.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

// Gemeinsame Logik fuer alle Aufrufe: Adresse zusammensetzen, senden, Fehler
// in lesbare deutsche Meldungen uebersetzen, Antwort als Daten (JSON) liefern.
async function request(path, options) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch (networkError) {
    // Das Backend antwortet gar nicht, z. B. weil es nicht gestartet ist.
    throw new Error(
      `Backend nicht erreichbar unter ${API_BASE_URL}. Läuft "uvicorn app.main:app --port 8000"?`
    );
  }
  if (!response.ok) {
    // Das Backend antwortet, meldet aber einen Fehler (z. B. 502): Den
    // Fehlertext des Backends auslesen und weitergeben.
    const text = await response.text().catch(() => "");
    let detail = text;
    try { const j = JSON.parse(text); if (typeof j.detail === "string") detail = j.detail; } catch (e) { /* kein JSON */ }
    throw new Error(`Backend-Fehler (${response.status}): ${detail || response.statusText}`);
  }
  return response.json();
}

// Die vier Arten von Aufrufen, die die Anwendung braucht:
export const getJson = (path) => request(path);                              // Daten abrufen
export const deleteJson = (path) => request(path, { method: "DELETE" });     // etwas loeschen
export const postJson = (path, body) =>                                      // Daten senden
  request(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
// Datei-Upload (multipart). Der Browser setzt den Content-Type selbst.
export const postFile = (path, file) => {
  const form = new FormData();
  form.append("file", file);
  return request(path, { method: "POST", body: form });
};
