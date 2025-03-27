from typing import Optional
from contextlib import AsyncExitStack
from ..application.repositories.service_repository import ServiceRepository
from .service_repository_impl import InMemoryServiceRepository
from ..interface_adapters.presenters.service_presenter import ServicePresenter
from ..application.get_service_interactor import GetServiceInteractor
from ..application.create_service_interactor import CreateServiceInteractor
from .logging_context import get_contextual_logger

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
            logger.debug("Created new Container instance")
        return cls._instance

    async def init_resources(self):
        """Initialize container resources."""
        if not self._exit_stack:
            logger.info("Initializing container resources")
            self._exit_stack = AsyncExitStack()
            if not self._repository:
                self._repository = InMemoryServiceRepository()

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

    def get_repository(self) -> ServiceRepository:
        """Get the service repository instance."""
        if not self._repository:
            logger.warning("Repository accessed before initialization")
            self._repository = InMemoryServiceRepository()
        return self._repository

    def get_service_presenter(self) -> ServicePresenter:
        """Get a new service presenter instance."""
        return ServicePresenter()

    def get_get_service_interactor(self) -> GetServiceInteractor:
        """Get a new get service interactor instance."""
        return GetServiceInteractor(
            repository=self.get_repository(), output_port=self.get_service_presenter()
        )

    def get_create_service_interactor(self) -> CreateServiceInteractor:
        """Get a new create service interactor instance."""
        return CreateServiceInteractor(
            repository=self.get_repository(), output_port=self.get_service_presenter()
        )
