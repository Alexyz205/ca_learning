"""Health controller implementing REST endpoints for health checks."""

from datetime import datetime
import psutil
from fastapi import APIRouter, Request

from ...infrastructure.logging_context import get_contextual_logger, operation_context
from ..dtos.health_dto import HealthResponse, HealthDetailedResponse, SystemMetrics

logger = get_contextual_logger(__name__)

# Track application start time for uptime calculation
_start_time = datetime.utcnow()


class HealthController:
    """Controller for health-related endpoints."""

    def __init__(self):
        """Initialize controller and routes."""
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        """Register all routes for this controller."""
        self.router.add_api_route(
            "/health",
            self.health_check,
            methods=["GET"],
            response_model=HealthResponse,
        )
        self.router.add_api_route(
            "/health/detailed",
            self.detailed_health_check,
            methods=["GET"],
            response_model=HealthDetailedResponse,
        )

    async def health_check(self, request: Request) -> HealthResponse:
        """Basic health check endpoint."""
        with operation_context("health_check", logger):
            logger.info("Processing health check request")
            response = HealthResponse(
                status="ok", timestamp=datetime.utcnow(), version="1.0.0"
            )
            logger.debug("Health check completed", extra={"status": response.status})
            return response

    async def detailed_health_check(self, request: Request) -> HealthDetailedResponse:
        """Detailed health check endpoint with system metrics."""
        with operation_context("detailed_health_check", logger):
            logger.info("Processing detailed health check request")
            try:
                metrics = self._get_system_metrics()
                logger.debug(
                    "System metrics collected",
                    extra={
                        "cpu_usage": metrics.cpu_usage,
                        "memory_usage": metrics.memory_usage,
                        "disk_usage": metrics.disk_usage,
                    },
                )
                now = datetime.utcnow()
                uptime = (now - _start_time).total_seconds()
                response = HealthDetailedResponse(
                    status="ok",
                    timestamp=now,
                    version="1.0.0",
                    uptime=uptime,
                    services={"database": "ok", "cache": "ok"},
                    system_metrics=metrics,
                )
                logger.info(
                    "Detailed health check completed",
                    extra={"status": response.status, "uptime": uptime},
                )
                return response
            except Exception as e:
                logger.error("Health check failed", extra={"error": str(e)})
                return HealthDetailedResponse(
                    status="error",
                    timestamp=datetime.utcnow(),
                    version="1.0.0",
                    uptime=0,
                    services={"database": "unknown", "cache": "unknown"},
                    system_metrics=SystemMetrics(
                        cpu_usage=0, memory_usage=0, disk_usage=0
                    ),
                )

    @staticmethod
    def _get_system_metrics() -> SystemMetrics:
        """Get current system metrics."""
        return SystemMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage("/").percent,
        )
