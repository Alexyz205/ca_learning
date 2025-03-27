import logging
from typing import Optional, List
from ...application.get_service_output_port import GetServiceOutputPort
from ...application.create_service_output_port import CreateServiceOutputPort
from ...interface_adapters.dtos.service_dto import ServiceDTO
from ...interface_adapters.dtos.service_response_dto import ServiceResponseDTO
from ...infrastructure.logging_context import get_contextual_logger, operation_context

logger = get_contextual_logger(__name__)


class ServicePresenter(GetServiceOutputPort, CreateServiceOutputPort):
    """Presenter for service-related outputs."""

    def __init__(self):
        self.response: Optional[ServiceResponseDTO] = None
        self.responses: List[ServiceResponseDTO] = []
        self.error: Optional[str] = None
        logger.debug("Initialized ServicePresenter")

    def _to_response_dto(self, dto: ServiceDTO) -> ServiceResponseDTO:
        """Convert internal DTO to response DTO."""
        with operation_context(
            "convert_to_response_dto", logger, service_id=str(dto.id)
        ):
            try:
                return ServiceResponseDTO(
                    id=dto.id,
                    name=dto.name,
                    description=dto.description,
                    created_at=dto.created_at,
                    updated_at=dto.updated_at,
                    is_active=dto.is_active,
                )
            except Exception as e:
                logger.error(
                    "Error converting DTO to response",
                    extra={"error": str(e), "service_id": str(dto.id)},
                )
                raise

    def present_service(self, service: Optional[ServiceDTO]) -> None:
        """Present a single service."""
        with operation_context("present_service", logger):
            if service:
                try:
                    logger.debug(
                        "Presenting service", extra={"service_id": str(service.id)}
                    )
                    self.response = self._to_response_dto(service)
                except Exception as e:
                    logger.error("Error presenting service", extra={"error": str(e)})
                    self.error = str(e)
            else:
                logger.warning("Attempted to present None service")
                self.error = "Service not found"
                self.response = None

    def present_services(self, services: List[ServiceDTO]) -> None:
        """Present multiple services."""
        with operation_context("present_services", logger, count=len(services)):
            try:
                self.responses = [self._to_response_dto(s) for s in services]
                logger.info(f"Presented {len(services)} services")
            except Exception as e:
                logger.error("Error presenting services", extra={"error": str(e)})
                self.error = str(e)
                self.responses = []

    def present_error(self, message: str) -> None:
        """Present an error message."""
        with operation_context("present_error", logger):
            logger.warning("Presenting error", extra={"message": message})
            self.error = message
            self.response = None
            self.responses = []

    def present_created_service(self, service: ServiceDTO) -> None:
        """Present the created service."""
        with operation_context(
            "present_created_service", logger, service_id=str(service.id)
        ):
            try:
                logger.info(
                    "Presenting created service",
                    extra={"service_id": str(service.id), "name": service.name},
                )
                self.response = self._to_response_dto(service)
            except Exception as e:
                logger.error(
                    "Error presenting created service", extra={"error": str(e)}
                )
                self.error = str(e)

    def present_creation_error(self, message: str) -> None:
        """Present an error that occurred during service creation."""
        with operation_context("present_creation_error", logger):
            logger.warning("Presenting creation error", extra={"message": message})
            self.error = message
            self.response = None
