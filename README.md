# Clean Architecture Service

A service implementing Clean Architecture principles in Python.

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

### Project Structure

```
src/
├── config/          # Configuration and settings
├── domain/         # Business logic and entities
├── infrastructure/ # External interfaces implementations
├── interface_adapters/ # Controllers and presenters
└── usecases/      # Application business rules
```

### Testing

Tests are organized into:
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`

Run tests with coverage reporting:
```bash
make test
```

### Environment Variables

- `SERVICE_HOST`: Host to bind the service (default: "0.0.0.0")
- `SERVICE_PORT`: Port to run the service (default: 8000)
- `SERVICE_DEBUG`: Enable debug mode (default: false)

### Available Endpoints

- `GET /health`: Basic health check
- `GET /health/detailed`: Detailed health status with metrics
- `GET /metrics`: Prometheus metrics
- `GET /v1/services`: List all services
- `POST /v1/services`: Create a new service
- `GET /v1/services/{id}`: Get service by ID