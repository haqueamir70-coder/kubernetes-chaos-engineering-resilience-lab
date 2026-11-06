"""Observable FastAPI workload used as a safe chaos-engineering target."""
from time import perf_counter

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="Resilience Lab API", version="1.0.0")
REQUESTS = Counter("http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2.5, 5),
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started = perf_counter()
        response = await call_next(request)
        REQUESTS.labels(request.method, request.url.path, str(response.status_code)).inc()
        LATENCY.labels(request.method, request.url.path).observe(perf_counter() - started)
        return response


app.add_middleware(MetricsMiddleware)


@app.get("/")
def index():
    return {
        "service": "resilience-api",
        "status": "ok",
        "message": "Resilience is demonstrated through measured recovery.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/work")
def work():
    return {"result": "completed"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
