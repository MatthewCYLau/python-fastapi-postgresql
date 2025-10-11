import time
from fastapi import Request
from api.config.logging import get_logger
from api.metrics.metrics import (
    REQUEST_COUNT,
    REQUEST_IN_PROGRESS,
    REQUEST_LATENCY,
)

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = get_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path
        REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        status = response.status_code
        REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
        REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(
            duration
        )
        REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

        return response


class RequestHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("User-Agent")
        logger.info(user_agent)
        response = await call_next(request)
        return response
