from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from ...usecases.service_dto import ServiceDTO


class ServiceResponseDTO(BaseModel):
    """DTO for service responses in the REST API."""

    id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)
    created_at: datetime
    updated_at: datetime
    is_active: bool

    @classmethod
    def from_dto(cls, dto: ServiceDTO) -> "ServiceResponseDTO":
        """Create a response model from a service DTO."""
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            is_active=dto.is_active,
        )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Example Service",
                "description": "A sample service description",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "is_active": True,
            }
        }


class ServiceListResponseDTO(BaseModel):
    """DTO for service list responses in the REST API."""

    services: List[ServiceResponseDTO] = []


class CreateServiceRequestDTO(BaseModel):
    """DTO for service creation requests in the REST API."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "name": "New Service",
                "description": "Description of the new service",
            }
        }
