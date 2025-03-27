import logging
from typing import Optional, List
from uuid import UUID
from ..application.repositories.service_repository import ServiceRepository
from ..domain.exceptions import ServiceNotFoundError
from ..domain.service_entity import Service
from ..domain.ports.logger_port import LoggerPort, LoggingContextPort
from ..domain.ports.metrics_port import MetricsPort
from .get_service_input_port import GetServiceInputPort
from .get_service_output_port import GetServiceOutputPort
from ..interface_adapters.dtos.service_dto import ServiceDTO


class GetServiceInteractor(GetServiceInputPort):
    """Implementation of the get service use case."""

    def __init__(
        self,
        repository: ServiceRepository,
        output_port: GetServiceOutputPort,
        logger: LoggerPort,
        logging_context: LoggingContextPort,
        metrics: MetricsPort,
    ):
        """Initialize with required dependencies."""
        self.repository = repository
        self.output_port = output_port
        self.logger = logger
        self.logging_context = logging_context
        self.metrics = metrics
        self.logger.debug("Initialized GetServiceInteractor")

    def get_service(self, service_id: UUID) -> Optional[ServiceDTO]:
        """Get a service by ID and present it through the output port."""
        with self.logging_context.operation_context(
            "get_service", self.logger, service_id=str(service_id)
        ):
            try:
                # Get the domain entity from repository
                service = self.repository.get_by_id(service_id)

                # Convert domain entity to DTO for crossing the boundary
                dto = ServiceDTO.from_domain(service)

                # Present the DTO through the output port
                self.output_port.present_service(dto)
                return dto

            except ServiceNotFoundError as e:
                self.logger.warning("Service not found", error=str(e))
                self.output_port.present_error(str(e))
                return None
            except Exception as e:
                self.logger.error("Error getting service", error=str(e))
                self.output_port.present_error(f"Internal error: {str(e)}")
                return None

    def get_all_services(self) -> List[ServiceDTO]:
        """Get all services and present them through the output port."""
        with self.logging_context.operation_context("get_all_services", self.logger):
            try:
                # Get all domain entities from repository
                services = self.repository.get_all()

                # Convert domain entities to DTOs for crossing the boundary
                dtos = [ServiceDTO.from_domain(service) for service in services]

                # Update metric for total number of services
                self.metrics.set_gauge("services_count", len(dtos))
                self.logger.info("Retrieved services", count=len(dtos))

                # Present DTOs through the output port
                self.output_port.present_services(dtos)
                return dtos

            except Exception as e:
                self.logger.error("Error getting all services", error=str(e))
                self.output_port.present_error(f"Internal error: {str(e)}")
                return []
