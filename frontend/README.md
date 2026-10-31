# Requirements Assistant – Frontend v2

Start: `npm install`, dann `npm run dev` (http://localhost:5173).

- Startseite mit zwei Bereichen: Anforderungen generieren (Wizard) und Virtual Buddy.
- Wizard: Eingabe → Epics → Anforderungen → Akzeptanzkriterien → Zusammenfassung. Alles editierbar, Status Entwurf/Bestätigt/Verworfen.
- Templates sind Daten (`src/templates/templates.js`) und austauschbar (Einstellungen).
- Generierung ist Mock (`src/services/generationService.js`, TODO Backend-Anbindung).
- Anmeldung, Jira-Übergabe und Wissensbasis-Suche sind Platzhalter.
- Backend (`/api/chat`) wird vom Buddy-Chat genutzt, falls es läuft (`VITE_API_BASE_URL`).
