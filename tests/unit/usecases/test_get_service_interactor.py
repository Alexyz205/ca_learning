import pytest
from uuid import UUID
from src.application.get_service_interactor import GetServiceInteractor
from src.domain.service_entity import Service
from src.domain.exceptions import ServiceNotFoundError
from tests.unit.usecases.mocks import (
    MockServiceRepository,
    MockGetServiceOutputPort,
    MockLoggerPort,
    MockLoggingContextPort,
    MockMetricsPort,
)


def test_get_service_success(service_entity):
    """Test successfully getting a service by ID."""
    # Given
    repository = MockServiceRepository()
    output_port = MockGetServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()
    repository.save(service_entity)

    # When
    interactor = GetServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.get_service(service_entity.id)

    # Then
    assert result is not None
    assert isinstance(result, Service)  # Verify we get a domain entity
    assert result.id == service_entity.id
    assert result.name == service_entity.name
    assert result.description == service_entity.description

    # Verify the repository was called
    assert repository.get_by_id_called is True

    # Verify the output port was called with correct domain entity
    assert output_port.presented_service is not None
    assert isinstance(output_port.presented_service, Service)  # Verify domain entity
    assert output_port.presented_service.id == service_entity.id
    assert output_port.error is None


def test_get_service_not_found():
    """Test getting a non-existent service by ID."""
    # Given
    repository = MockServiceRepository()
    output_port = MockGetServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = GetServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.get_service(UUID("00000000-0000-0000-0000-000000000000"))

    # Then
    assert result is None

    # Verify the repository was called
    assert repository.get_by_id_called is True

    # Verify the output port was called with an error
    assert output_port.presented_service is None
    assert output_port.error is not None
    assert "not found" in output_port.error.lower()


def test_get_all_services(service_entity):
    """Test getting all services."""
    # Given
    repository = MockServiceRepository()
    output_port = MockGetServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()
    repository.save(service_entity)

    # When
    interactor = GetServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.get_all_services()

    # Then
    assert len(result) == 1
    assert isinstance(result[0], Service)  # Verify we get domain entities
    assert result[0].id == service_entity.id

    # Verify the repository was called
    assert repository.get_all_called is True

    # Verify the output port was called with correct domain entities
    assert output_port.presented_services is not None
    assert len(output_port.presented_services) == 1
    assert isinstance(output_port.presented_services[0], Service)  # Verify domain entity
    assert output_port.presented_services[0].id == service_entity.id


def test_get_all_services_empty():
    """Test getting all services when there are none."""
    # Given
    repository = MockServiceRepository()
    output_port = MockGetServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = GetServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.get_all_services()

    # Then
    assert len(result) == 0

    # Verify the repository was called
    assert repository.get_all_called is True

    # Verify the output port was called with empty list
    assert output_port.presented_services is not None
    assert len(output_port.presented_services) == 0
