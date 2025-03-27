from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ..domain.service_entity import Service


class GetServiceInputPort(ABC):
    """Input port interface for getting service details."""

    @abstractmethod
    def get_service(self, service_id: UUID) -> Optional[Service]:
        """Get service by ID."""
        pass

    @abstractmethod
    def get_all_services(self) -> List[Service]:
        """Get all services."""
        pass
