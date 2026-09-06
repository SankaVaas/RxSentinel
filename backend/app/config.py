"""Centralized application settings, loaded from environment variables."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    # LLM
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-6"

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # External clinical data APIs
    rxnorm_api_base: str = "https://rxnav.nlm.nih.gov/REST"
    openfda_api_base: str = "https://api.fda.gov"
    dailymed_api_base: str = "https://dailymed.nlm.nih.gov/dailymed/services/v2"

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
