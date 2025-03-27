from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest
from src.config.settings import Settings
from src.infrastructure.container import Container
from src.infrastructure.middleware import setup_middlewares
from src.infrastructure.logging_context import get_contextual_logger
from src.interface_adapters.controller_factory import ControllerFactory
from src.domain.exceptions import (
    ServiceNotFoundError,
    ServiceValidationError,
    ServiceAlreadyExistsError,
)

logger = get_contextual_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # The container is now injected from the AppServer
    logger.info("Starting application lifecycle")

    # Check if container is already provided
    if not hasattr(app.state, "container"):
        logger.warning("Container not provided to the application, creating a new one")
        app.state.container = Container()

    # Initialize container resources
    await app.state.container.init_resources()
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

    # Set up middleware using the dedicated function
    setup_middlewares(app, settings)

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

    # Initialize a temporary container for initial setup
    # The actual container will be injected by the AppServer later
    container = app.state.container if hasattr(app.state, "container") else Container()

    # Use the controller factory to register controllers
    ControllerFactory.create_and_register_controllers(app, container)

    return app
