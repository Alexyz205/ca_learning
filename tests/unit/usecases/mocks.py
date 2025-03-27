from typing import Optional, List, Callable
from uuid import UUID

from src.domain.service_entity import Service
from src.domain.exceptions import ServiceNotFoundError
from src.application.repositories.service_repository import ServiceRepository
from src.application.get_service_output_port import GetServiceOutputPort
from src.application.create_service_output_port import CreateServiceOutputPort
from src.interface_adapters.dtos.service_dto import ServiceDTO  # Updated import
from src.domain.ports.metrics_port import MetricsPort
from src.domain.ports.logger_port import LoggerPort, LoggingContextPort
from contextlib import contextmanager


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

    def get_by_id(self, service_id: UUID) -> Service:
        self.get_by_id_called = True
        service = self.services.get(service_id)
        if not service:
            raise ServiceNotFoundError(f"Service with ID {service_id} not found")
        return service

    def get_all(self) -> List[Service]:
        self.get_all_called = True
        return list(self.services.values())

    def update(self, service: Service) -> Service:
        self.update_called = True
        if service.id not in self.services:
            raise ServiceNotFoundError(f"Service with ID {service.id} not found")
        self.services[service.id] = service
        return service

    def delete(self, service_id: UUID) -> bool:
        self.delete_called = True
        if service_id not in self.services:
            raise ServiceNotFoundError(f"Service with ID {service_id} not found")
        del self.services[service_id]
        return True


class MockGetServiceOutputPort(GetServiceOutputPort):
    """Mock implementation of GetServiceOutputPort for testing."""

    def __init__(self):
        self.presented_service = None
        self.presented_services = None
        self.error = None

    def present_service(self, service: Optional[Service]) -> None:
        self.presented_service = service

    def present_services(self, services: List[Service]) -> None:
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


class MockMetricsPort(MetricsPort):
    """Mock implementation of MetricsPort for testing."""

    def increment_counter(self, name: str, value: float = 1, **labels) -> None:
        """Mock implementation of increment_counter."""
        pass

    def set_gauge(self, name: str, value: float, **labels) -> None:
        """Mock implementation of set_gauge."""
        pass

    def observe_histogram(self, name: str, value: float, **labels) -> None:
        """Mock implementation of observe_histogram."""
        pass

    def track_operation(self, operation_name: str) -> Callable[[Callable], Callable]:
        """Mock implementation of track_operation."""

        def decorator(func):
            return func

        return decorator


class MockLoggerPort(LoggerPort):
    """Mock implementation of LoggerPort for testing."""

    def debug(self, message: str, **kwargs) -> None:
        """Mock implementation of debug."""
        pass

    def info(self, message: str, **kwargs) -> None:
        """Mock implementation of info."""
        pass

    def warning(self, message: str, **kwargs) -> None:
        """Mock implementation of warning."""
        pass

    def error(self, message: str, **kwargs) -> None:
        """Mock implementation of error."""
        pass


class MockLoggingContextPort(LoggingContextPort):
    """Mock implementation of LoggingContextPort for testing."""

    @contextmanager
    def operation_context(
        self, operation_name: str, logger: LoggerPort, **context_data
    ):
        """Mock implementation of operation_context."""
        yield
