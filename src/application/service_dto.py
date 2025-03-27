from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class ServiceDTO:
    """Data Transfer Object for service use cases."""

    id: Optional[UUID] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
