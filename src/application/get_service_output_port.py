from abc import ABC, abstractmethod
from typing import Optional, List
from ..interface_adapters.dtos.service_dto import ServiceDTO


class GetServiceOutputPort(ABC):
    """Output port interface for presenting service details."""

    @abstractmethod
    def present_service(self, service: Optional[ServiceDTO]) -> None:
        """Present a single service."""
        pass

    @abstractmethod
    def present_services(self, services: List[ServiceDTO]) -> None:
        """Present multiple services."""
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """Present an error message."""
        pass
