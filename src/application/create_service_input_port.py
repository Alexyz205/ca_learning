from abc import ABC, abstractmethod
from ..interface_adapters.dtos.service_dto import ServiceDTO


class CreateServiceInputPort(ABC):
    """Input port interface for creating a service."""

    @abstractmethod
    def create_service(self, name: str, description: str) -> ServiceDTO:
        """Create a new service."""
        pass
