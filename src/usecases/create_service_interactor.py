from ..domain.service_repository import ServiceRepository
from ..domain.service_entity import Service
from ..domain.exceptions import ServiceValidationError, ServiceAlreadyExistsError
from .create_service_input_port import CreateServiceInputPort
from .create_service_output_port import CreateServiceOutputPort
from .service_dto import ServiceDTO
from ..infrastructure.logging_context import get_contextual_logger, operation_context
from ..infrastructure.metrics import SERVICES_COUNT
from ..infrastructure.metrics_decorator import track_operation

logger = get_contextual_logger(__name__)

class CreateServiceInteractor(CreateServiceInputPort):
    """Implementation of the create service use case."""

    def __init__(self, repository: ServiceRepository, output_port: CreateServiceOutputPort):
        self.repository = repository
        self.output_port = output_port
        logger.debug("Initialized CreateServiceInteractor")

    @track_operation("create_service")
    def create_service(self, name: str, description: str) -> ServiceDTO:
        """Create a new service and present it through the output port."""
        with operation_context("create_service", logger, service_name=name):
            try:
                # Basic validation
                if not name:
                    raise ServiceValidationError("Service name cannot be empty")
                if len(name) > 100:
                    raise ServiceValidationError("Service name too long")
                if len(description) > 500:
                    raise ServiceValidationError("Service description too long")
                
                # Create and save the service
                service = Service.create(name=name, description=description)
                logger.debug("Created service entity", extra={"service_id": str(service.id)})
                
                saved_service = self.repository.save(service)
                logger.info("Saved service", extra={
                    "service_id": str(saved_service.id),
                    "name": saved_service.name
                })
                
                # Increment the services count metric
                try:
                    current = SERVICES_COUNT._value.get()
                    if current is not None:
                        SERVICES_COUNT.set(current + 1)
                    else:
                        SERVICES_COUNT.set(1)
                except Exception as e:
                    logger.warning("Failed to update services count metric", extra={"error": str(e)})
                
                # Create DTO and present response
                dto = ServiceDTO(
                    id=saved_service.id,
                    name=saved_service.name,
                    description=saved_service.description,
                    created_at=saved_service.created_at,
                    updated_at=saved_service.updated_at,
                    is_active=saved_service.is_active
                )
                self.output_port.present_created_service(dto)
                return dto
                
            except ServiceValidationError as e:
                logger.warning("Service validation failed", extra={"error": str(e)})
                self.output_port.present_creation_error(str(e))
                return ServiceDTO()
                
            except ServiceAlreadyExistsError as e:
                logger.error("Service already exists", extra={"error": str(e)})
                self.output_port.present_creation_error(str(e))
                return ServiceDTO()
                
            except Exception as e:
                logger.error("Unexpected error creating service", extra={"error": str(e)})
                self.output_port.present_creation_error(f"Internal error: {str(e)}")
                return ServiceDTO()