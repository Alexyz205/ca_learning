import pytest
from uuid import UUID

from src.domain.exceptions import ServiceNotFoundError, ServiceAlreadyExistsError
from src.infrastructure.service_repository_impl import InMemoryServiceRepository


def test_save_service(service_entity):
    """Test saving a service to the repository."""
    # Given
    repository = InMemoryServiceRepository()

    # When
    saved_service = repository.save(service_entity)

    # Then
    assert saved_service.id == service_entity.id
    assert saved_service.name == service_entity.name
    assert saved_service.description == service_entity.description


def test_get_service_by_id(service_entity):
    """Test retrieving a service by ID."""
    # Given
    repository = InMemoryServiceRepository()
    repository.save(service_entity)

    # When
    retrieved_service = repository.get_by_id(service_entity.id)

    # Then
    assert retrieved_service is not None
    assert retrieved_service.id == service_entity.id
    assert retrieved_service.name == service_entity.name


def test_get_service_by_id_not_found():
    """Test retrieving a non-existent service by ID raises an exception."""
    # Given
    repository = InMemoryServiceRepository()

    # When / Then
    with pytest.raises(ServiceNotFoundError):
        repository.get_by_id(UUID("00000000-0000-0000-0000-000000000000"))


def test_get_all_services(service_entity):
    """Test retrieving all services."""
    # Given
    repository = InMemoryServiceRepository()
    repository.save(service_entity)

    # When
    services = repository.get_all()

    # Then
    assert len(services) == 1
    assert services[0].id == service_entity.id


def test_get_all_services_empty():
    """Test retrieving all services when there are none."""
    # Given
    repository = InMemoryServiceRepository()

    # When
    services = repository.get_all()

    # Then
    assert len(services) == 0


def test_update_service(service_entity):
    """Test updating a service."""
    # Given
    repository = InMemoryServiceRepository()
    repository.save(service_entity)

    # Update the service
    service_entity.name = "Updated Service"
    service_entity.description = "Updated description"

    # When
    updated_service = repository.update(service_entity)

    # Then
    assert updated_service.name == "Updated Service"
    assert updated_service.description == "Updated description"

    # Verify the update was persisted
    retrieved_service = repository.get_by_id(service_entity.id)
    assert retrieved_service.name == "Updated Service"
    assert retrieved_service.description == "Updated description"


def test_update_nonexistent_service(service_entity):
    """Test updating a non-existent service raises an exception."""
    # Given
    repository = InMemoryServiceRepository()

    # When / Then
    with pytest.raises(ServiceNotFoundError):
        repository.update(service_entity)


def test_delete_service(service_entity):
    """Test deleting a service."""
    # Given
    repository = InMemoryServiceRepository()
    repository.save(service_entity)

    # When
    result = repository.delete(service_entity.id)

    # Then
    assert result is True

    # Verify the service was deleted
    with pytest.raises(ServiceNotFoundError):
        repository.get_by_id(service_entity.id)


def test_delete_nonexistent_service():
    """Test deleting a non-existent service raises an exception."""
    # Given
    repository = InMemoryServiceRepository()

    # When / Then
    with pytest.raises(ServiceNotFoundError):
        repository.delete(UUID("00000000-0000-0000-0000-000000000000"))


def test_save_duplicate_service(service_entity):
    """Test saving a service with the same ID raises an exception."""
    # Given
    repository = InMemoryServiceRepository()
    repository.save(service_entity)

    # When / Then
    with pytest.raises(ServiceAlreadyExistsError):
        repository.save(service_entity)
