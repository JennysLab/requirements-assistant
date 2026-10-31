# Betrieb als Container

Der Prototyp lässt sich als ein einziges Container-Paket betreiben, lokal wie in der Cloud (AWS EC2). Frontend und Backend laufen dabei unter **einer** Adresse.

## Aufbau

| Datei | Aufgabe |
|---|---|
| `Dockerfile` | Baut zuerst das Frontend (Node), dann das Backend (Python), das das fertige Frontend mit ausliefert. |
| `docker-compose.yml` | Startet den Container mit einem Befehl, bindet Port 8000 und zwei dauerhafte Speicherbereiche ein (Wissensbasis, Protokolle). |
| `.dockerignore` | Hält Geheimnisse (`.env`), Bibliotheksordner und lokale Daten aus dem Paket. |

## Wichtige Entscheidungen

- **Eine Adresse:** Das Backend liefert das gebaute Frontend aus (`FRONTEND_DIST`). Dadurch entfallen CORS-Freigaben, und Testpersonen brauchen nur einen Link.
- **Keine Schlüssel im Paket:** Anthropic-Schlüssel und Jira-Token stehen nie im Container-Abbild. Sie kommen zur Laufzeit aus `backend/.env` (siehe `docker-compose.yml`).
- **Dauerhafte Daten:** Die Wissensbasis (Chroma, `/data`) und die Protokolle liegen in benannten Volumes und überstehen Neustarts und Neubauten.
- **Einbettungsmodell vorab geladen:** Das Modell der Wissensbasis wird beim Bau heruntergeladen, damit der erste Upload nicht hängt.
- **Benutzer ohne Administratorrechte:** Der Prozess läuft im Container als normaler Benutzer.
- **Lokale Entwicklung bleibt unverändert:** Ohne `FRONTEND_DIST` verhält sich das Backend wie bisher, das Frontend läuft über `npm run dev`.

## Starten

```
docker compose up -d --build
```

Danach: http://localhost:8000 (Gesundheitsprüfung: http://localhost:8000/api/health, API-Dokumentation: http://localhost:8000/docs).

Vorher die Datei `backend/.env` aus `backend/.env.example` anlegen und die Werte eintragen.

Stoppen: `docker compose down` (die Daten bleiben erhalten). Alles inklusive Daten löschen: `docker compose down -v`.

## Stand der Prüfung

Frontend-Build, Auslieferung durch das Backend (Seiten, Dateien, 404 für unbekannte API-Adressen, kein Zugriff außerhalb des Frontend-Ordners) und die 17 Tests wurden ohne Container geprüft. Der Bau des Container-Abbilds selbst ist noch nicht auf einem echten Docker-System getestet.
