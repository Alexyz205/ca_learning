import logging
import time
import uuid
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .metrics import PrometheusMiddleware
from .logging_context import get_contextual_logger, request_id

logger = get_contextual_logger(__name__)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware for tracking requests with unique IDs and logging."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID and set in context
        req_id = str(uuid.uuid4())
        request.state.request_id = req_id
        request_id.set(req_id)

        # Start timing the request
        start_time = time.time()

        # Log the incoming request with context
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host if request.client else None,
            },
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate request duration
            duration = time.time() - start_time

            # Add request ID to response headers
            response.headers["X-Request-ID"] = req_id

            # Log the completed request with context
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": int(duration * 1000),
                },
            )

            return response

        except Exception as e:
            # Log any unhandled exceptions with context
            logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "duration_ms": int((time.time() - start_time) * 1000),
                },
            )
            raise
        finally:
            # Clear request ID from context
            request_id.set(None)


def setup_middlewares(app: FastAPI, settings=None) -> None:
    """Set up all application middlewares."""
    # Add metrics middleware first to capture all requests
    app.add_middleware(PrometheusMiddleware)

    # Add request tracking middleware
    app.add_middleware(RequestTrackingMiddleware)

    # Add CORS middleware if settings are provided
    if settings:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allow_origins,
            allow_credentials=settings.cors_allow_credentials,
            allow_methods=settings.cors_allow_methods,
            allow_headers=settings.cors_allow_headers,
        )
