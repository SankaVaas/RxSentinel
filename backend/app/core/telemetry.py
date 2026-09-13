"""OpenTelemetry instrumentation. Langfuse tracing is wired in at the agent-run
level (see app/services/interaction_service.py) so that each LangGraph node
shows up as a span with its inputs/outputs — this is what the AgentTraceViewer
in the frontend renders."""
import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)


def configure_telemetry(app: FastAPI, settings) -> None:
    resource = Resource(attributes={SERVICE_NAME: "rxsentinel-backend"})
    provider = TracerProvider(resource=resource)

    if settings.otel_exporter_otlp_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )

            exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)
        except ImportError:
            logger.warning("OTLP exporter not installed; falling back to console.")
            exporter = ConsoleSpanExporter()
    else:
        exporter = ConsoleSpanExporter()

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
