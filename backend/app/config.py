"""Centralized application settings, loaded from environment variables."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    # LLM
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Drug reference / interaction data
    rxnorm_api_base: str = "https://rxnav.nlm.nih.gov/REST"
    drug_interactions_csv_path: str = "data/drug_interactions.csv"

    # Auth
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_client_id: str | None = None

    # Observability
    otel_exporter_otlp_endpoint: str | None = None
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None

    # CORS
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()