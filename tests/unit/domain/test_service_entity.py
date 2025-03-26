from datetime import datetime
from uuid import UUID
import pytest
from src.domain.service_entity import Service

def test_service_creation():
    """Test service creation with factory method."""
    # When
    name = "Test Service"
    description = "A test service"
    service = Service.create(name=name, description=description)
    
    # Then
    assert isinstance(service, Service)
    assert isinstance(service.id, UUID)
    assert service.name == name
    assert service.description == description
    assert isinstance(service.created_at, datetime)
    assert isinstance(service.updated_at, datetime)
    assert service.is_active is True

def test_service_attributes():
    """Test service attributes can be accessed correctly."""
    # Given
    service = Service(
        id=UUID('123e4567-e89b-12d3-a456-426614174000'),
        name="Test Service",
        description="A test service",
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2023, 1, 1),
        is_active=True
    )
    
    # Then
    assert service.id == UUID('123e4567-e89b-12d3-a456-426614174000')
    assert service.name == "Test Service"
    assert service.description == "A test service"
    assert service.created_at == datetime(2023, 1, 1)
    assert service.updated_at == datetime(2023, 1, 1)
    assert service.is_active is True