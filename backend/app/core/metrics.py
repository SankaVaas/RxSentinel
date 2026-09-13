"""Prometheus metrics: request counts/latency and agent-run outcomes."""
from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    "rxsentinel_http_requests_total", "Total HTTP requests", ["method", "path", "status_code"]
)
http_request_duration_seconds = Histogram(
    "rxsentinel_http_request_duration_seconds", "HTTP request latency", ["method", "path"]
)
agent_runs_total = Counter(
    "rxsentinel_agent_runs_total", "Total agent runs", ["status"]
)
agent_findings_total = Counter(
    "rxsentinel_agent_findings_total", "Total interaction findings produced", ["severity", "status"]
)