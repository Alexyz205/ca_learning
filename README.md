# Clean Architecture Service

A robust microservice implementing Clean Architecture principles in Python with FastAPI.

## Project Overview

This project demonstrates the implementation of Clean Architecture in a Python microservice, providing a service management API. It showcases how to organize code into distinct layers with clear separation of concerns, resulting in a codebase that is maintainable, testable, and flexible.

## Clean Architecture Implementation

This project rigorously follows the Clean Architecture pattern with four distinct layers:

### 1. Domain Layer (`src/domain/`)
- Contains enterprise business rules and entities
- Defines repository interfaces (e.g., `ServiceRepository`)
- Includes domain entities (e.g., `Service`) and domain exceptions
- Independent of frameworks, databases, or external concerns
- Example: `service_entity.py` defines the core Service entity with factory methods

### 2. Use Cases Layer (`src/application/`)
- Contains application-specific business logic
- Implements input and output ports using interfaces
- Orchestrates flows of data between domain entities and external interfaces
- Examples:
  - `create_service_interactor.py`: Handles service creation logic
  - `get_service_interactor.py`: Handles service retrieval logic

### 3. Interface Adapters Layer (`src/interface_adapters/`)
- Converts data between use case and external formats
- Includes controllers, presenters, and DTOs
- Examples:
  - `controllers/service_rest_controller.py`: REST API controllers
  - `dtos/service_response_dto.py`: Data transfer objects

### 4. Infrastructure Layer (`src/infrastructure/`)
- Contains implementations of interfaces defined in inner layers
- Framework-specific code, database implementations, external services
- Examples:
  - `rest_server.py`: FastAPI server configuration
  - `service_repository_impl.py`: In-memory implementation of the repository
  - `container.py`: Dependency injection container
  - `logging_context.py`: Contextual logging support
  - `metrics.py` and `metrics_decorator.py`: Metrics tracking

## Features

### Core Features
- **Service Management**: Create, retrieve, and list services
- **Health Checks**: Basic and detailed health status endpoints
- **Metrics**: Prometheus-compatible metrics exposure
- **Containerization**: Docker and Docker Compose support

### Technical Features
- **Contextual Logging**: Request-scoped logging with correlation IDs
- **Dependency Injection**: Clean dependency management with container pattern
- **Metrics Collection**: Performance and operational metrics
- **Middleware**: Request processing middleware
- **Error Handling**: Comprehensive domain and application error handling
- **Configuration Management**: YAML and environment-based configuration

## Development

### Development Container
This project includes a devcontainer configuration for VS Code. To use it:
1. Install the "Remote - Containers" extension in VS Code
2. Open the project in VS Code
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command
4. VS Code will build and start the development container with all necessary tools

### Manual Development
If you prefer not to use VS Code's devcontainer, you can use Docker Compose directly:

```bash
# Build all images
make build

# Run tests
make test

# Start development server
make dev

# Start production server
make prod

# Clean up containers and build artifacts
make clean
```

## Project Structure

```
src/
├── config/                # Configuration and settings
│   ├── logging_config.py  # Logging configuration
│   ├── service_config.yaml# Service configuration
│   └── settings.py        # Application settings
├── domain/                # Business logic and entities
│   ├── exceptions.py      # Domain exceptions
│   ├── service_entity.py  # Core Service entity
│   └── service_repository.py # Repository interfaces
├── infrastructure/        # External interfaces implementations
│   ├── container.py       # Dependency injection container
│   ├── dependency_context.py # Context management for dependencies
│   ├── logging_context.py # Contextual logging
│   ├── metrics_decorator.py # Metrics collection decorators
│   ├── metrics.py         # Prometheus metrics definitions
│   ├── middleware.py      # Request middleware
│   ├── rest_server.py     # FastAPI server setup
│   └── service_repository_impl.py # Implementation of repositories
├── interface_adapters/    # Controllers and presenters
│   ├── controllers/       # API controllers
│   │   ├── health_controller.py # Health check endpoints
│   │   └── service_rest_controller.py # Service API endpoints
│   ├── dtos/              # Data transfer objects
│   └── presenters/        # Response formatters
└── application/             # Application business rules
    ├── create_service_input_port.py # Input port for service creation
    ├── create_service_interactor.py # Implementation of service creation
    ├── create_service_output_port.py # Output port for service creation
    ├── get_service_input_port.py # Input port for service retrieval
    ├── get_service_interactor.py # Implementation of service retrieval
    ├── get_service_output_port.py # Output port for service retrieval
    └── service_dto.py     # DTOs for use cases
```

## Testing

Tests are organized into:
- **Unit tests**: `tests/unit/` - Tests for individual components
- **Integration tests**: `tests/integration/` - Tests for component interactions

Run tests with coverage reporting:
```bash
make test
# or
./run_tests.sh
```

## Configuration

### Environment Variables
- `SERVICE_HOST`: Host to bind the service (default: "0.0.0.0")
- `SERVICE_PORT`: Port to run the service (default: 8000)
- `SERVICE_DEBUG`: Enable debug mode (default: false)

### Config Files
- `src/config/service_config.yaml`: Main service configuration
- `src/config/logging_config.py`: Logging configuration

## API Endpoints

### Service Management
- `GET /v1/services`: List all services
- `POST /v1/services`: Create a new service
- `GET /v1/services/{id}`: Get service by ID

### Monitoring
- `GET /health`: Basic health check
- `GET /health/detailed`: Detailed health status with metrics
- `GET /metrics`: Prometheus metrics

## Running the Application

### Using Make Commands
```bash
# Development mode
make dev

# Production mode
make prod
```

### Direct Execution
```bash
python src/main.py
```