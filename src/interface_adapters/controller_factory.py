"""Factory for creating controllers with proper dependencies."""

from fastapi import FastAPI
from src.infrastructure.container import Container
from src.interface_adapters.controllers.service_rest_controller import ServiceController
from src.interface_adapters.controllers.health_controller import HealthController


class ControllerFactory:
    """Factory for creating and registering controllers."""

    @staticmethod
    def create_and_register_controllers(app: FastAPI, container: Container) -> None:
        """Create controllers with proper dependencies and register them with the app."""
        # Create controllers with dependencies from the container
        service_controller = ServiceController(
            create_service_interactor=container.get_create_service_interactor(),
            get_service_interactor=container.get_get_service_interactor(),
        )

        health_controller = HealthController()

        # Register routers with versioning
        app.include_router(
            health_controller.router
        )  # Health check endpoints without version prefix
        app.include_router(
            service_controller.router, prefix="/v1/services"
        )  # Version 1 API endpoints
