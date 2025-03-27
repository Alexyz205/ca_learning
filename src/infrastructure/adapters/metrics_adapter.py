"""Adapter that implements the metrics port interface using the actual metrics implementation."""

from typing import Callable
from functools import wraps
from ...domain.ports.metrics_port import MetricsPort
from ..metrics import (
    SERVICE_OPERATION_LATENCY,
    SERVICE_OPERATIONS,
    SERVICES_COUNT,
)
from ..metrics_decorator import track_operation as actual_track_operation


class MetricsAdapter(MetricsPort):
    """Adapter for metrics functionality."""

    def increment_counter(self, name: str, value: float = 1, **labels) -> None:
        """Increment a counter metric."""
        if name == "operation_count":
            SERVICE_OPERATIONS.labels(**labels).inc(value)
        # Add other counters as needed

    def set_gauge(self, name: str, value: float, **labels) -> None:
        """Set a gauge metric."""
        if name == "services_count":
            SERVICES_COUNT.set(value)
        # Add other gauges as needed

    def observe_histogram(self, name: str, value: float, **labels) -> None:
        """Observe a value for a histogram metric."""
        if name == "operation_duration_seconds":
            SERVICE_OPERATION_LATENCY.labels(**labels).observe(value)
        # Add other histograms as needed

    def track_operation(self, operation_name: str) -> Callable[[Callable], Callable]:
        """Create decorator to track operation metrics."""
        return actual_track_operation(operation_name)


def get_metrics() -> MetricsPort:
    """Get a metrics adapter."""
    return MetricsAdapter()
