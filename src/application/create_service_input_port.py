from abc import ABC, abstractmethod
from ..domain.service_entity import Service


class CreateServiceInputPort(ABC):
    """Input port interface for creating a service."""

    @abstractmethod
    def create_service(self, name: str, description: str) -> Service:
        """Create a new service."""
        pass
