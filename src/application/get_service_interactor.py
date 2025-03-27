import logging
from typing import Optional
from uuid import UUID

from ..application.repositories.service_repository import ServiceRepository
from ..domain.exceptions import ServiceNotFoundError
from .get_service_input_port import GetServiceInputPort
from .get_service_output_port import GetServiceOutputPort
from .service_dto import ServiceDTO
from ..infrastructure.logging_context import get_contextual_logger, operation_context
from ..infrastructure.metrics import SERVICES_COUNT
from ..infrastructure.metrics_decorator import track_operation

logger = get_contextual_logger(__name__)


class GetServiceInteractor(GetServiceInputPort):
    """Implementation of the get service use case."""

    def __init__(
        self, repository: ServiceRepository, output_port: GetServiceOutputPort
    ):
        self.repository = repository
        self.output_port = output_port
        logger.debug("Initialized GetServiceInteractor")

    @track_operation("get_service")
    def get_service(self, service_id: UUID) -> Optional[ServiceDTO]:
        """Get a service by ID and present it through the output port."""
        with operation_context("get_service", logger, service_id=str(service_id)):
            try:
                service = self.repository.get_by_id(service_id)
                dto = ServiceDTO(
                    id=service.id,
                    name=service.name,
                    description=service.description,
                    created_at=service.created_at,
                    updated_at=service.updated_at,
                    is_active=service.is_active,
                )
                self.output_port.present_service(dto)
                return dto
            except ServiceNotFoundError as e:
                logger.warning(f"Service not found", extra={"error": str(e)})
                self.output_port.present_error(str(e))
                return None
            except Exception as e:
                logger.error("Error getting service", extra={"error": str(e)})
                self.output_port.present_error(f"Internal error: {str(e)}")
                return None

    @track_operation("get_all_services")
    def get_all_services(self) -> list[ServiceDTO]:
        """Get all services and present them through the output port."""
        with operation_context("get_all_services", logger):
            try:
                services = self.repository.get_all()
                dtos = [
                    ServiceDTO(
                        id=service.id,
                        name=service.name,
                        description=service.description,
                        created_at=service.created_at,
                        updated_at=service.updated_at,
                        is_active=service.is_active,
                    )
                    for service in services
                ]

                # Update metric for total number of services
                SERVICES_COUNT.set(len(dtos))

                logger.info("Retrieved services", extra={"count": len(dtos)})
                self.output_port.present_services(dtos)
                return dtos
            except Exception as e:
                logger.error("Error getting all services", extra={"error": str(e)})
                self.output_port.present_error(f"Internal error: {str(e)}")
                return []
