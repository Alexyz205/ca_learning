"""Logger port that defines the interface for logging functionality."""

from abc import ABC, abstractmethod


class LoggerPort(ABC):
    """Abstract interface for logging functionality."""

    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        """Log a debug message."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        pass


class ContextManagerPort(ABC):
    """Abstract interface for operation context management."""

    @abstractmethod
    def __enter__(self) -> None:
        """Enter the context."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context."""
        pass


class LoggingContextPort(ABC):
    """Abstract interface for operation context logging."""

    @abstractmethod
    def operation_context(
        self, operation_name: str, logger: LoggerPort, **context_data
    ) -> ContextManagerPort:
        """Create an operation context with the given name and context data."""
        pass
