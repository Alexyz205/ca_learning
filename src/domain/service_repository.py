from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from .service_entity import Service

class ServiceRepository(ABC):
    """Abstract interface for service repository operations."""
    
    @abstractmethod
    def save(self, service: Service) -> Service:
        """Save a service to the repository."""
        pass
    
    @abstractmethod
    def get_by_id(self, service_id: UUID) -> Optional[Service]:
        """Retrieve a service by its ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Service]:
        """Retrieve all services."""
        pass
    
    @abstractmethod
    def update(self, service: Service) -> Service:
        """Update an existing service."""
        pass
    
    @abstractmethod
    def delete(self, service_id: UUID) -> bool:
        """Delete a service by its ID."""
        pass