import pytest
from src.application.create_service_interactor import CreateServiceInteractor
from src.domain.service_entity import Service  # Updated import
from tests.unit.usecases.mocks import (
    MockServiceRepository,
    MockCreateServiceOutputPort,
    MockLoggerPort,
    MockLoggingContextPort,
    MockMetricsPort,
)


def test_create_service_success(service_data):
    """Test successfully creating a service."""
    # Given
    repository = MockServiceRepository()
    output_port = MockCreateServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = CreateServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.create_service(
        name=service_data["name"], description=service_data["description"]
    )

    # Then
    assert result is not None
    assert isinstance(result, Service)  # Now expecting Service instead of ServiceDTO
    assert result.name == service_data["name"]
    assert result.description == service_data["description"]

    # Verify the repository was called
    assert repository.save_called is True

    # Verify the output port was called with correct data
    assert output_port.presented_service is not None
    assert output_port.presented_service.name == service_data["name"]
    assert output_port.error is None


def test_create_service_empty_name():
    """Test creating a service with an empty name."""
    # Given
    repository = MockServiceRepository()
    output_port = MockCreateServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = CreateServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.create_service(name="", description="Test Description")

    # Then
    assert result is not None
    assert result.name == ""  # Empty service should have empty name
    assert result.description == ""  # Empty service should have empty description

    # Verify the repository was not called
    assert repository.save_called is False

    # Verify the output port was called with an error
    assert output_port.presented_service is None
    assert output_port.error is not None
    assert "name cannot be empty" in output_port.error.lower()


def test_create_service_name_too_long():
    """Test creating a service with a name that's too long."""
    # Given
    repository = MockServiceRepository()
    output_port = MockCreateServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = CreateServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.create_service(
        name="a" * 101, description="Test Description"  # 101 characters
    )

    # Then
    assert result is not None
    assert result.name == ""  # Empty service should have empty name
    assert result.description == ""  # Empty service should have empty description

    # Verify the repository was not called
    assert repository.save_called is False

    # Verify the output port was called with an error
    assert output_port.presented_service is None
    assert output_port.error is not None
    assert "name too long" in output_port.error.lower()


def test_create_service_description_too_long():
    """Test creating a service with a description that's too long."""
    # Given
    repository = MockServiceRepository()
    output_port = MockCreateServiceOutputPort()
    logger = MockLoggerPort()
    logging_context = MockLoggingContextPort()
    metrics = MockMetricsPort()

    # When
    interactor = CreateServiceInteractor(
        repository=repository,
        output_port=output_port,
        logger=logger,
        logging_context=logging_context,
        metrics=metrics,
    )
    result = interactor.create_service(
        name="Test Name", description="a" * 501  # 501 characters
    )

    # Then
    assert result is not None
    assert result.name == ""  # Empty service should have empty name
    assert result.description == ""  # Empty service should have empty description

    # Verify the repository was not called
    assert repository.save_called is False

    # Verify the output port was called with an error
    assert output_port.presented_service is None
    assert output_port.error is not None
    assert "description too long" in output_port.error.lower()
