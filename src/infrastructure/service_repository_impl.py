import logging
from typing import Optional, List, Dict
from uuid import UUID

from ..interface_adapters.repositories.service_repository import ServiceRepository
from ..domain.service_entity import Service
from ..domain.exceptions import ServiceNotFoundError, ServiceAlreadyExistsError
from .logging_context import get_contextual_logger, operation_context
from .metrics_decorator import track_operation

logger = get_contextual_logger(__name__)


class InMemoryServiceRepository(ServiceRepository):
    """In-memory implementation of the service repository."""

    def __init__(self):
        self._services: Dict[UUID, Service] = {}
        logger.info("Initialized InMemoryServiceRepository")

    @track_operation("repository_save")
    def save(self, service: Service) -> Service:
        """Save a service to the in-memory store."""
        with operation_context("repository_save", logger, service_id=str(service.id)):
            if service.id in self._services:
                logger.error(
                    "Service already exists",
                    extra={"service_id": str(service.id), "name": service.name},
                )
                raise ServiceAlreadyExistsError(
                    f"Service with ID {service.id} already exists"
                )

            logger.info(
                "Saving service",
                extra={"service_id": str(service.id), "name": service.name},
            )
            self._services[service.id] = service
            return service

    @track_operation("repository_get_by_id")
    def get_by_id(self, service_id: UUID) -> Optional[Service]:
        """Retrieve a service by its ID from the in-memory store."""
        with operation_context(
            "repository_get_by_id", logger, service_id=str(service_id)
        ):
            logger.debug("Fetching service", extra={"service_id": str(service_id)})
            service = self._services.get(service_id)
            if not service:
                logger.warning(
                    "Service not found", extra={"service_id": str(service_id)}
                )
                raise ServiceNotFoundError(f"Service with ID {service_id} not found")
            return service

    @track_operation("repository_get_all")
    def get_all(self) -> List[Service]:
        """Retrieve all services from the in-memory store."""
        with operation_context("repository_get_all", logger):
            services = list(self._services.values())
            logger.debug("Fetched all services", extra={"count": len(services)})
            return services

    @track_operation("repository_update")
    def update(self, service: Service) -> Service:
        """Update an existing service in the in-memory store."""
        with operation_context("repository_update", logger, service_id=str(service.id)):
            if service.id not in self._services:
                logger.error(
                    "Service not found for update",
                    extra={"service_id": str(service.id)},
                )
                raise ServiceNotFoundError(f"Service with ID {service.id} not found")

            logger.info(
                "Updating service",
                extra={"service_id": str(service.id), "name": service.name},
            )
            self._services[service.id] = service
            return service

    @track_operation("repository_delete")
    def delete(self, service_id: UUID) -> bool:
        """Delete a service from the in-memory store."""
        with operation_context("repository_delete", logger, service_id=str(service_id)):
            if service_id not in self._services:
                logger.warning(
                    "Service not found for deletion",
                    extra={"service_id": str(service_id)},
                )
                raise ServiceNotFoundError(f"Service with ID {service_id} not found")

            logger.info("Deleting service", extra={"service_id": str(service_id)})
            del self._services[service_id]
            return True
