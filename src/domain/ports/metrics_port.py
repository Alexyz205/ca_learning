"""Metrics port defining the interface for metrics functionality."""
from abc import ABC, abstractmethod
from typing import Callable


class MetricsPort(ABC):
    """Abstract interface for metrics functionality."""

    @abstractmethod
    def increment_counter(self, name: str, value: float = 1, **labels) -> None:
        """Increment a counter metric."""
        pass

    @abstractmethod
    def set_gauge(self, name: str, value: float, **labels) -> None:
        """Set a gauge metric."""
        pass

    @abstractmethod
    def observe_histogram(self, name: str, value: float, **labels) -> None:
        """Observe a value for a histogram metric."""
        pass

    @abstractmethod
    def track_operation(
        self, operation_name: str
    ) -> Callable[[Callable], Callable]:
        """Create decorator to track operation metrics."""
        pass