from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.service_entity import Service


class GetServiceOutputPort(ABC):
    """Output port interface for presenting service details."""

    @abstractmethod
    def present_service(self, service: Optional[Service]) -> None:
        """Present a single service."""
        pass

    @abstractmethod
    def present_services(self, services: List[Service]) -> None:
        """Present multiple services."""
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """Present an error message."""
        pass
