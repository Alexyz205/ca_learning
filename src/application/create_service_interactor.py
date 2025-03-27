from ..application.repositories.service_repository import ServiceRepository
from ..domain.service_entity import Service
from ..domain.exceptions import ServiceValidationError, ServiceAlreadyExistsError
from ..domain.ports.logger_port import LoggerPort, LoggingContextPort
from ..domain.ports.metrics_port import MetricsPort
from .create_service_input_port import CreateServiceInputPort
from .create_service_output_port import CreateServiceOutputPort
from ..interface_adapters.dtos.service_dto import ServiceDTO


class CreateServiceInteractor(CreateServiceInputPort):
    """Implementation of the create service use case."""

    def __init__(
        self,
        repository: ServiceRepository,
        output_port: CreateServiceOutputPort,
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
        self.logger.debug("Initialized CreateServiceInteractor")

    @property
    def track_operation(self):
        """Get the track_operation decorator."""
        return self.metrics.track_operation("create_service")

    def create_service(self, name: str, description: str) -> ServiceDTO:
        """Create a new service and present it through the output port."""
        with self.logging_context.operation_context(
            "create_service", self.logger, service_name=name
        ):
            try:
                # Basic validation
                if not name:
                    raise ServiceValidationError("Service name cannot be empty")
                if len(name) > 100:
                    raise ServiceValidationError("Service name too long")
                if len(description) > 500:
                    raise ServiceValidationError("Service description too long")

                # Create and save the service as a domain entity
                service_entity = Service.create(name=name, description=description)
                self.logger.debug(
                    "Created service entity", service_id=str(service_entity.id)
                )

                # Save to repository and get domain entity back
                saved_service = self.repository.save(service_entity)
                self.logger.info(
                    "Saved service",
                    service_id=str(saved_service.id),
                    name=saved_service.name,
                )

                # Increment the services count metric
                try:
                    self.metrics.set_gauge(
                        "services_count", 1
                    )  # This will be handled by the adapter
                except Exception as e:
                    self.logger.warning(
                        "Failed to update services count metric", error=str(e)
                    )

                # Convert domain entity to DTO for crossing the boundary
                dto = ServiceDTO.from_domain(saved_service)

                # Present DTO through output port
                self.output_port.present_created_service(dto)
                return dto

            except ServiceValidationError as e:
                self.logger.warning("Service validation failed", error=str(e))
                self.output_port.present_creation_error(str(e))
                return ServiceDTO()
            except ServiceAlreadyExistsError as e:
                self.logger.error("Service already exists", error=str(e))
                self.output_port.present_creation_error(str(e))
                return ServiceDTO()
            except Exception as e:
                self.logger.error("Unexpected error creating service", error=str(e))
                self.output_port.present_creation_error(f"Internal error: {str(e)}")
                return ServiceDTO()
