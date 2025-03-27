"""Dependency injection container for clean architecture implementation."""

from typing import Optional
from contextlib import AsyncExitStack

# Domain and application interfaces
from ..application.repositories.service_repository import ServiceRepository
from ..domain.ports.logger_port import LoggerPort, LoggingContextPort
from ..domain.ports.metrics_port import MetricsPort

# Application use cases
from ..interface_adapters.presenters.service_presenter import ServicePresenter
from ..application.get_service_interactor import GetServiceInteractor
from ..application.create_service_interactor import CreateServiceInteractor

# Infrastructure implementations
from .service_repository_impl import InMemoryServiceRepository
from .adapters.logger_adapter import get_logger, get_logging_context
from .adapters.metrics_adapter import get_metrics
from .logging_context import get_contextual_logger

# Config
from ..config.settings import Settings

logger = get_contextual_logger(__name__)


class Container:
    """Dependency Injection Container with lifecycle management."""

    _instance: Optional["Container"] = None

    def __new__(cls):
        """Implement singleton pattern for testing."""
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance._repository = None
            cls._instance._exit_stack = None
            cls._instance._settings = None
            cls._instance._logger = None
            cls._instance._logging_context = None
            cls._instance._metrics = None
            logger.debug("Created new Container instance")
        return cls._instance

    async def init_resources(self):
        """Initialize container resources."""
        if not self._exit_stack:
            logger.info("Initializing container resources")
            self._exit_stack = AsyncExitStack()
            if not self._repository:
                self._repository = InMemoryServiceRepository()
            if not self._logger:
                self._logger = get_logger(__name__)
            if not self._logging_context:
                self._logging_context = get_logging_context()
            if not self._metrics:
                self._metrics = get_metrics()

    async def cleanup(self):
        """Cleanup container resources."""
        if self._exit_stack:
            logger.info("Cleaning up container resources")
            await self._exit_stack.aclose()
            self._exit_stack = None

    @classmethod
    def reset(cls):
        """Reset the container instance (for testing)."""
        if cls._instance and cls._instance._exit_stack:
            logger.info("Resetting container instance")
        cls._instance = None

    # Infrastructure Layer Dependencies

    def set_settings(self, settings: Settings) -> None:
        """Set application settings."""
        self._settings = settings

    def get_settings(self) -> Settings:
        """Get application settings."""
        return self._settings

    def get_repository(self) -> ServiceRepository:
        """Get the service repository instance."""
        if not self._repository:
            logger.warning("Repository accessed before initialization")
            self._repository = InMemoryServiceRepository()
        return self._repository

    def get_logger(self, module_name: str = __name__) -> LoggerPort:
        """Get a logger instance."""
        return get_logger(module_name)

    def get_logging_context(self) -> LoggingContextPort:
        """Get a logging context instance."""
        return get_logging_context()

    def get_metrics(self) -> MetricsPort:
        """Get a metrics instance."""
        return get_metrics()

    # Interface Adapters Layer Dependencies

    def get_service_presenter(self) -> ServicePresenter:
        """Get a new service presenter instance."""
        return ServicePresenter()

    # Application Layer Dependencies

    def get_get_service_interactor(self) -> GetServiceInteractor:
        """Get a new get service interactor instance."""
        return GetServiceInteractor(
            repository=self.get_repository(),
            output_port=self.get_service_presenter(),
            logger=self.get_logger("app.get_service"),
            logging_context=self.get_logging_context(),
            metrics=self.get_metrics(),
        )

    def get_create_service_interactor(self) -> CreateServiceInteractor:
        """Get a new create service interactor instance."""
        return CreateServiceInteractor(
            repository=self.get_repository(),
            output_port=self.get_service_presenter(),
            logger=self.get_logger("app.create_service"),
            logging_context=self.get_logging_context(),
            metrics=self.get_metrics(),
        )
