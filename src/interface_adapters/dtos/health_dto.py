"""DTOs for health check responses."""

from datetime import datetime
from pydantic import BaseModel


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
