from abc import ABC, abstractmethod
from ..domain.service_entity import Service


class CreateServiceOutputPort(ABC):
    """Output port interface for presenting the result of service creation."""

    @abstractmethod
    def present_created_service(self, service: Service) -> None:
        """Present the created service."""
        pass

    @abstractmethod
    def present_creation_error(self, message: str) -> None:
        """Present an error that occurred during service creation."""
        pass
