from abc import ABC, abstractmethod
from ..interface_adapters.dtos.service_dto import ServiceDTO


class CreateServiceOutputPort(ABC):
    """Output port interface for presenting the result of service creation."""

    @abstractmethod
    def present_created_service(self, service: ServiceDTO) -> None:
        """Present the created service."""
        pass

    @abstractmethod
    def present_creation_error(self, message: str) -> None:
        """Present an error that occurred during service creation."""
        pass
