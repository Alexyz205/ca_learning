from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from .service_dto import ServiceDTO

class GetServiceInputPort(ABC):
    """Input port interface for getting service details."""
    
    @abstractmethod
    def get_service(self, service_id: UUID) -> Optional[ServiceDTO]:
        """Get service by ID."""
        pass
    
    @abstractmethod
    def get_all_services(self) -> list[ServiceDTO]:
        """Get all services."""
        pass