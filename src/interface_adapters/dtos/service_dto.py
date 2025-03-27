"""Data transfer objects for services that cross architectural boundaries."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

from ...domain.service_entity import Service


@dataclass
class ServiceDTO:
    """Data Transfer Object for service use cases.

    This DTO is used for transferring service data between the application layer
    and interface adapters layer. It's designed to be serializable and independent
    of the domain model implementation.
    """

    id: Optional[UUID] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True

    @classmethod
    def from_domain(cls, service: Service) -> "ServiceDTO":
        """Create a DTO from a domain entity."""
        return cls(
            id=service.id,
            name=service.name,
            description=service.description,
            created_at=service.created_at,
            updated_at=service.updated_at,
            is_active=service.is_active,
        )

    def to_domain(self) -> Service:
        """Convert this DTO to a domain entity."""
        # Use the current datetime if created_at/updated_at are None
        now = datetime.utcnow()
        return Service(
            id=(
                self.id
                if self.id is not None
                else UUID("00000000-0000-0000-0000-000000000000")
            ),
            name=self.name,
            description=self.description,
            created_at=self.created_at if self.created_at is not None else now,
            updated_at=self.updated_at if self.updated_at is not None else now,
            is_active=self.is_active,
        )
