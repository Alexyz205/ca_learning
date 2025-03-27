from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
import psutil
from ...infrastructure.dependency_context import with_logging_context
from ...infrastructure.logging_context import get_contextual_logger, operation_context

router = APIRouter(tags=["health"])
logger = get_contextual_logger(__name__)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: str


class SystemMetrics(BaseModel):
    """System metrics for detailed health check."""

    cpu_usage: float
    memory_usage: float
    disk_usage: float


class HealthDetailedResponse(HealthResponse):
    """Detailed health check response model."""

    uptime: float
    services: dict[str, str]
    system_metrics: SystemMetrics


_start_time = datetime.utcnow()


def get_system_metrics() -> SystemMetrics:
    """Get current system metrics."""
    return SystemMetrics(
        cpu_usage=psutil.cpu_percent(),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage("/").percent,
    )


@router.get("/health", response_model=HealthResponse)
@with_logging_context
async def health_check(request: Request):
    """Basic health check endpoint."""
    with operation_context("health_check", logger):
        logger.info("Processing health check request")
        response = HealthResponse(
            status="ok", timestamp=datetime.utcnow(), version="1.0.0"
        )
        logger.debug("Health check completed", extra={"status": response.status})
        return response


@router.get("/health/detailed", response_model=HealthDetailedResponse)
@with_logging_context
async def detailed_health_check(request: Request):
    """Detailed health check endpoint with system metrics."""
    with operation_context("detailed_health_check", logger):
        logger.info("Processing detailed health check request")

        try:
            metrics = get_system_metrics()
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
                system_metrics=SystemMetrics(cpu_usage=0, memory_usage=0, disk_usage=0),
            )
