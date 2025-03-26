from typing import Optional, List
from uuid import UUID

from src.domain.service_entity import Service
from src.domain.service_repository import ServiceRepository
from src.usecases.get_service_output_port import GetServiceOutputPort
from src.usecases.create_service_output_port import CreateServiceOutputPort
from src.usecases.service_dto import ServiceDTO

class MockServiceRepository(ServiceRepository):
    """Mock implementation of ServiceRepository for testing."""
    
    def __init__(self):
        self.services = {}
        self.save_called = False
        self.get_by_id_called = False
        self.get_all_called = False
        self.update_called = False
        self.delete_called = False
        
    def save(self, service: Service) -> Service:
        self.save_called = True
        self.services[service.id] = service
        return service
        
    def get_by_id(self, service_id: UUID) -> Optional[Service]:
        self.get_by_id_called = True
        return self.services.get(service_id)
        
    def get_all(self) -> List[Service]:
        self.get_all_called = True
        return list(self.services.values())
        
    def update(self, service: Service) -> Service:
        self.update_called = True
        self.services[service.id] = service
        return service
        
    def delete(self, service_id: UUID) -> bool:
        self.delete_called = True
        if service_id in self.services:
            del self.services[service_id]
            return True
        return False

class MockGetServiceOutputPort(GetServiceOutputPort):
    """Mock implementation of GetServiceOutputPort for testing."""
    
    def __init__(self):
        self.presented_service = None
        self.presented_services = None
        self.error = None
        
    def present_service(self, service: Optional[ServiceDTO]) -> None:
        self.presented_service = service
        
    def present_services(self, services: List[ServiceDTO]) -> None:
        self.presented_services = services
        
    def present_error(self, message: str) -> None:
        self.error = message

class MockCreateServiceOutputPort(CreateServiceOutputPort):
    """Mock implementation of CreateServiceOutputPort for testing."""
    
    def __init__(self):
        self.presented_service = None
        self.error = None
        
    def present_created_service(self, service: ServiceDTO) -> None:
        self.presented_service = service
        
    def present_creation_error(self, message: str) -> None:
        self.error = message