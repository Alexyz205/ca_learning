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

    @property
    def track_operation(self):
        """Get the track_operation decorator."""
        return self.metrics.track_operation("get_service")

    def get_service(self, service_id: UUID) -> Optional[Service]:
        """Get a service by ID and present it through the output port."""
        with self.logging_context.operation_context(
            "get_service", self.logger, service_id=str(service_id)
        ):
            try:
                # Get the domain entity from repository
                service = self.repository.get_by_id(service_id)
                self.logger.debug("Retrieved service", service_id=str(service_id))

                # Present through the output port
                self.output_port.present_service(service)
                return service

            except ServiceNotFoundError as e:
                self.logger.warning("Service not found", error=str(e))
                self.output_port.present_error(str(e))
                return None
            except Exception as e:
                self.logger.error("Error getting service", error=str(e))
                self.output_port.present_error(f"Internal error: {str(e)}")
                return None

    def get_all_services(self) -> List[Service]:
        """Get all services and present them through the output port."""
        with self.logging_context.operation_context("get_all_services", self.logger):
            try:
                # Get all domain entities from repository
                services = self.repository.get_all()
                self.logger.info("Retrieved services", count=len(services))

                # Update metric for total number of services
                try:
                    self.metrics.set_gauge("services_count", len(services))
                except Exception as e:
                    self.logger.warning(
                        "Failed to update services count metric", error=str(e)
                    )

                # Present through the output port
                self.output_port.present_services(services)
                return services

            except Exception as e:
                self.logger.error("Error getting all services", error=str(e))
                self.output_port.present_error(f"Internal error: {str(e)}")
                return []
