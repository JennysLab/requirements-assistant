"""
Zentrale Konfiguration. Alle veraenderlichen Werte (API-Keys, Modellname,
erlaubte Frontend-Ursprünge, Jira-Zugang) kommen ausschliesslich aus
Umgebungsvariablen bzw. der .env-Datei - nichts davon ist im Code hart
codiert. Das ist die Voraussetzung dafuer, dass sich z. B. das Modell oder
die Umgebung (lokal/AWS) aendern laesst, ohne Code anzufassen.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5"
    cors_allow_origins: str = "http://localhost:5173"

    # Jira (Modul M2, Push). Leer = Jira-Push ist nicht eingerichtet.
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    jira_project_key: str = ""

    # extra="ignore": weitere Eintraege in der .env fuehren nicht zu einem Fehler.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    # lru_cache sorgt dafuer, dass die .env-Datei nur einmal gelesen wird,
    # nicht bei jedem Request neu.
    return Settings()
