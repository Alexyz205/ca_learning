from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Service:
    """Core domain entity representing a service."""
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    @staticmethod
    def create(name: str, description: str) -> 'Service':
        """Factory method to create a new service."""
        now = datetime.utcnow()
        return Service(
            id=uuid4(),
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            is_active=True
        )