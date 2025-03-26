from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from ..dtos.service_response_dto import ServiceListResponseDTO, ServiceResponseDTO
from ..dtos.service_request_dto import CreateServiceRequest
from ...infrastructure.dependency_context import with_logging_context
from ...infrastructure.logging_context import get_contextual_logger, operation_context
from ...usecases.get_service_interactor import GetServiceInteractor
from ...usecases.create_service_interactor import CreateServiceInteractor
from ...domain.exceptions import ServiceNotFoundError, ServiceValidationError
from ...infrastructure.container import Container

router = APIRouter(prefix="/services", tags=["services"])
logger = get_contextual_logger(__name__)

@with_logging_context
async def get_container(request: Request) -> Container:
    """Dependency provider for the container."""
    return Container()

@with_logging_context
async def get_get_service_interactor(
    container: Container = Depends(get_container)
) -> GetServiceInteractor:
    """Dependency provider for GetServiceInteractor."""
    return container.get_get_service_interactor()

@with_logging_context
async def get_create_service_interactor(
    container: Container = Depends(get_container)
) -> CreateServiceInteractor:
    """Dependency provider for CreateServiceInteractor."""
    return container.get_create_service_interactor()

def validate_service_input(name: str, description: str) -> None:
    """Validate service input data."""
    if not name:
        raise ServiceValidationError("Service name cannot be empty")
    if len(name) > 100:
        raise ServiceValidationError("Service name too long")
    if len(description) > 500:
        raise ServiceValidationError("Service description too long")

@router.post("", response_model=ServiceResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_service(request: Request, create_request: CreateServiceRequest) -> ServiceResponseDTO:
    """Create a new service."""
    with operation_context("create_service_endpoint", logger):
        try:
            container = request.app.state.container
            interactor = container.get_create_service_interactor()
            result = interactor.create_service(
                name=create_request.name,
                description=create_request.description
            )
            
            if not result or not result.id:
                raise ServiceValidationError("Failed to create service")
                
            return ServiceResponseDTO.from_dto(result)
            
        except ServiceValidationError as e:
            logger.error("Failed to create service", extra={"error": str(e)})
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": str(e)}
            )
        except Exception as e:
            logger.error("Unexpected error creating service", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

@router.get("/{service_id}", response_model=ServiceResponseDTO)
async def get_service(request: Request, service_id: UUID) -> ServiceResponseDTO:
    """Get a service by ID."""
    with operation_context("get_service_endpoint", logger, service_id=str(service_id)):
        try:
            container = request.app.state.container
            interactor = container.get_get_service_interactor()
            result = interactor.get_service(service_id)
            
            if not result:
                logger.error("Failed to get service", extra={"service_id": str(service_id)})
                raise ServiceNotFoundError(f"Service with ID {service_id} not found")
                
            return ServiceResponseDTO.from_dto(result)
            
        except ServiceNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            logger.error("Unexpected error getting service", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

@router.get("", response_model=ServiceListResponseDTO)
async def get_all_services(request: Request) -> ServiceListResponseDTO:
    """Get all services."""
    with operation_context("get_all_services_endpoint", logger):
        try:
            container = request.app.state.container
            interactor = container.get_get_service_interactor()
            results = interactor.get_all_services()
            return ServiceListResponseDTO(services=[ServiceResponseDTO.from_dto(dto) for dto in results])
        except Exception as e:
            logger.error("Unexpected error getting all services", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )