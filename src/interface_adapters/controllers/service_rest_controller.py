"""Service controller implementing REST endpoints for services."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from ...application.get_service_interactor import GetServiceInteractor
from ...application.create_service_interactor import CreateServiceInteractor
from ...domain.exceptions import ServiceNotFoundError, ServiceValidationError
from ...interface_adapters.dtos.service_response_dto import (
    ServiceListResponseDTO,
    ServiceResponseDTO,
)
from ...interface_adapters.dtos.service_request_dto import CreateServiceRequest
from ...infrastructure.logging_context import get_contextual_logger, operation_context

# Create router without prefix - prefix will be added when included in the app
router = APIRouter()
logger = get_contextual_logger(__name__)


class ServiceController:
    """Controller for service-related endpoints following Clean Architecture."""

    def __init__(
        self,
        create_service_interactor: CreateServiceInteractor,
        get_service_interactor: GetServiceInteractor,
    ):
        """Initialize with required use cases."""
        self.create_service_interactor = create_service_interactor
        self.get_service_interactor = get_service_interactor
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        """Register all routes for this controller."""
        self.router.add_api_route(
            "",
            self.create_service,
            methods=["POST"],
            response_model=ServiceResponseDTO,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/{service_id}",
            self.get_service,
            methods=["GET"],
            response_model=ServiceResponseDTO,
        )
        self.router.add_api_route(
            "",
            self.get_all_services,
            methods=["GET"],
            response_model=ServiceListResponseDTO,
        )

    async def create_service(
        self, request: Request, create_request: CreateServiceRequest
    ) -> ServiceResponseDTO:
        """Create a new service."""
        with operation_context("create_service_endpoint", logger):
            try:

                result = self.create_service_interactor.create_service(
                    name=create_request.name, description=create_request.description
                )

                if not result or not result.id:
                    raise ServiceValidationError("Failed to create service")

                return ServiceResponseDTO.from_dto(result)

            except ServiceValidationError as e:
                logger.error("Failed to create service", extra={"error": str(e)})
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
                )
            except Exception as e:
                logger.error(
                    "Unexpected error creating service", extra={"error": str(e)}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )

    async def get_service(
        self, request: Request, service_id: UUID
    ) -> ServiceResponseDTO:
        """Get a service by ID."""
        with operation_context(
            "get_service_endpoint", logger, service_id=str(service_id)
        ):
            try:
                result = self.get_service_interactor.get_service(service_id)

                if not result:
                    logger.error(
                        "Failed to get service", extra={"service_id": str(service_id)}
                    )
                    raise ServiceNotFoundError(
                        f"Service with ID {service_id} not found"
                    )

                return ServiceResponseDTO.from_dto(result)

            except ServiceNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                )
            except Exception as e:
                logger.error(
                    "Unexpected error getting service", extra={"error": str(e)}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )

    async def get_all_services(self, request: Request) -> ServiceListResponseDTO:
        """Get all services."""
        with operation_context("get_all_services_endpoint", logger):
            try:
                results = self.get_service_interactor.get_all_services()
                return ServiceListResponseDTO(
                    services=[ServiceResponseDTO.from_dto(dto) for dto in results]
                )
            except Exception as e:
                logger.error(
                    "Unexpected error getting all services", extra={"error": str(e)}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
