from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest
from src.config.settings import Settings
from src.infrastructure.container import Container
from src.infrastructure.middleware import RequestTrackingMiddleware
from src.infrastructure.metrics import PrometheusMiddleware
from src.infrastructure.logging_context import get_contextual_logger
from src.interface_adapters.controllers.service_rest_controller import (
    router as service_router,
)
from src.interface_adapters.controllers.health_controller import router as health_router
from src.domain.exceptions import (
    ServiceNotFoundError,
    ServiceValidationError,
    ServiceAlreadyExistsError,
)

logger = get_contextual_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    container = Container()
    logger.info("Starting application")
    app.state.container = container
    await container.init_resources()
    logger.info("Application started successfully")

    yield  # Application runs here

    logger.info("Shutting down application")
    if hasattr(app.state, "container"):
        await app.state.container.cleanup()
    logger.info("Application shutdown complete")


def create_app(settings: Settings) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Add metrics middleware first to capture all requests
    app.add_middleware(PrometheusMiddleware)

    # Add request tracking middleware
    app.add_middleware(RequestTrackingMiddleware)

    # Add CORS middleware with configuration from settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Register exception handlers
    @app.exception_handler(ServiceNotFoundError)
    async def service_not_found_handler(request: Request, exc: ServiceNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ServiceValidationError)
    async def service_validation_error_handler(
        request: Request, exc: ServiceValidationError
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(ServiceAlreadyExistsError)
    async def service_already_exists_handler(
        request: Request, exc: ServiceAlreadyExistsError
    ):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    # Add metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Expose Prometheus metrics."""
        return PlainTextResponse(generate_latest())

    # Register routers with versioning
    app.include_router(health_router)  # Health check endpoints without version prefix
    app.include_router(service_router, prefix="/v1")  # Version 1 API endpoints

    return app
