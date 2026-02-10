"""
Debug Tracing Middleware (v3).
Adds request_id and timing for structured observability.
"""

from __future__ import annotations

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class DebugTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        request.state.start_time = time.monotonic()
        response = await call_next(request)
        duration_ms = (time.monotonic() - request.state.start_time) * 1000
        response.headers["X-Request-Id"] = request.state.request_id
        response.headers["X-Process-Time-ms"] = f"{duration_ms:.2f}"
        return response
