import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from src.config.settings import Settings
from src.infrastructure.rest_server import create_app
from src.infrastructure.container import Container


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

    # Create test client
    with TestClient(app) as client:
        yield client
        # Reset container after each test to ensure clean state
        Container.reset()


@pytest.fixture
def created_service(test_client):
    """Fixture to create a test service and return its data."""
    service_data = {
        "name": "Test Integration Service",
        "description": "A service created during integration testing",
    }

    response = test_client.post("/v1/services", json=service_data)
    assert response.status_code == 201
    return response.json()


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_detailed_health_check(test_client):
    """Test the detailed health check endpoint."""
    response = test_client.get("/health/detailed")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data
    assert "services" in data
    assert "system_metrics" in data


def test_metrics_endpoint(test_client):
    """Test the metrics endpoint."""
    response = test_client.get("/metrics")

    assert response.status_code == 200
    # Prometheus metrics are plain text
    assert "http_requests_total" in response.text


def test_create_service(test_client):
    """Test creating a new service."""
    service_data = {
        "name": "Test Integration Service",
        "description": "A service created during integration testing",
    }

    response = test_client.post("/v1/services", json=service_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == service_data["name"]
    assert data["description"] == service_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert data["is_active"] is True


def test_get_service_by_id(test_client, created_service):
    """Test getting a service by ID."""
    service_id = created_service["id"]
    response = test_client.get(f"/v1/services/{service_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id
    assert data["name"] == created_service["name"]
    assert data["description"] == created_service["description"]


def test_get_service_not_found(test_client):
    """Test getting a non-existent service."""
    non_existent_id = str(uuid4())
    response = test_client.get(f"/v1/services/{non_existent_id}")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_get_all_services(test_client, created_service):
    """Test getting all services."""
    response = test_client.get("/v1/services")

    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert isinstance(data["services"], list)
    assert len(data["services"]) >= 1
    assert any(s["id"] == created_service["id"] for s in data["services"])


def test_create_service_invalid_input(test_client):
    """Test creating a service with invalid input."""
    # Empty name
    service_data = {"name": "", "description": "A service with an empty name"}

    response = test_client.post("/v1/services", json=service_data)
    assert response.status_code == 422  # FastAPI's default validation error status
    data = response.json()
    assert "detail" in data

    # Name too long
    service_data = {
        "name": "a" * 101,  # 101 characters
        "description": "A service with a name that's too long",
    }

    response = test_client.post("/v1/services", json=service_data)
    assert response.status_code == 422  # FastAPI's default validation error status
    data = response.json()
    assert "detail" in data
