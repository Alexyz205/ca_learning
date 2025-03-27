import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient

from src.config.settings import Settings
from src.infrastructure.rest_server import create_app
from src.infrastructure.container import Container


@pytest.fixture(autouse=True)
def clean_container():
    """Reset the container before each test."""
    Container.reset()
    yield
    Container.reset()


@pytest.fixture
def test_client():
    """Fixture for FastAPI test client."""
    # Create settings with test configuration
    settings = Settings(
        debug=True,
        app_name="Test Clean Architecture Service",
        host="127.0.0.1",
        port=8000,
    )

    # Create the FastAPI app
    app = create_app(settings)

    # Initialize container
    container = Container()

    # Create test client
    with TestClient(app) as client:
        yield client


@pytest.fixture
def service_id():
    """Fixture for a service ID."""
    return uuid4()


@pytest.fixture
def service_data():
    """Fixture for service data."""
    return {"name": "Test Service", "description": "A test service for unit tests"}


@pytest.fixture
def service_entity(service_id):
    """Fixture for a service entity."""
    from src.domain.service_entity import Service

    now = datetime.utcnow()
    return Service(
        id=service_id,
        name="Test Service",
        description="A test service for unit tests",
        created_at=now,
        updated_at=now,
        is_active=True,
    )


@pytest.fixture
def service_dto(service_id):
    """Fixture for a service DTO."""
    from src.application.service_dto import ServiceDTO

    now = datetime.utcnow()
    return ServiceDTO(
        id=service_id,
        name="Test Service",
        description="A test service for unit tests",
        created_at=now,
        updated_at=now,
        is_active=True,
    )
