"""RxSentinel FastAPI application entrypoint."""
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.logging import configure_logging
from app.core.metrics import http_request_duration_seconds, http_requests_total
from app.core.telemetry import configure_telemetry

settings = get_settings()
configure_logging(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_telemetry(app, settings)
    yield


app = FastAPI(
    title="RxSentinel API",
    description="Agentic drug-drug interaction & polypharmacy safety system.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    duration = time.monotonic() - start
    path = request.url.path
    http_requests_total.labels(request.method, path, response.status_code).inc()
    http_request_duration_seconds.labels(request.method, path).observe(duration)
    return response


app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["meta"])
async def health() -> dict:
    """Liveness: process is up. Does not check dependencies -- see /health/ready."""
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/ready", tags=["meta"])
async def readiness() -> Response:
    """Readiness: checks DB connectivity, for k8s readinessProbe / load balancer."""
    try:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
        return Response(content='{"status":"ready"}', media_type="application/json")
    except Exception as exc:  # noqa: BLE001
        return Response(
            content=f'{{"status":"not_ready","error":"{exc}"}}',
            media_type="application/json",
            status_code=503,
        )


@app.get("/metrics", tags=["meta"])
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)