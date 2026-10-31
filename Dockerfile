# Container fuer den Requirements Assistant: Frontend und Backend in einem Paket.
# Zwei Stufen: Stufe 1 baut das Frontend, Stufe 2 ist das Backend, das das
# fertig gebaute Frontend mit ausliefert. So gibt es nur eine Adresse.

# ---- Stufe 1: Frontend bauen (Node) ----
FROM node:20-slim AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# Leer = das Frontend ruft das Backend unter derselben Adresse auf wie die Seite selbst.
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# ---- Stufe 2: Backend (Python) ----
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FRONTEND_DIST=/app/frontend_dist \
    KNOWLEDGE_DIR=/data/chroma

# Eigener Benutzer ohne Administratorrechte (Sicherheit).
RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app/backend /data/chroma \
    && chown -R app:app /app /data

WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Einbettungsmodell der Wissensbasis schon beim Bau laden. Sonst haengt der
# erste Upload, bis das Modell heruntergeladen ist.
USER app
RUN python -c "from chromadb.utils.embedding_functions import DefaultEmbeddingFunction; DefaultEmbeddingFunction()(['Vorwaermen'])"

COPY --chown=app:app backend/ ./
COPY --from=frontend --chown=app:app /build/dist /app/frontend_dist
# Protokolle der Generierung (siehe app/generation/logs); als Volume dauerhaft haltbar.
RUN mkdir -p /app/backend/app/generation/logs

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health', timeout=4)" || exit 1

# Schluessel (Anthropic, Jira) stehen NICHT im Paket; sie kommen zur Laufzeit
# ueber Umgebungsvariablen bzw. die Datei backend/.env (siehe docker-compose.yml).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
