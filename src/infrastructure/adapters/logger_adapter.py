"""Adapter that implements the logger port interface using the actual logging implementation."""

from ...domain.ports.logger_port import (
    LoggerPort,
    ContextManagerPort,
    LoggingContextPort,
)
from ..logging_context import get_contextual_logger as actual_get_logger
from ..logging_context import operation_context as actual_operation_context


class LoggerAdapter(LoggerPort):
    """Adapter for the logging functionality."""

    def __init__(self, module_name: str):
        """Initialize with the module name."""
        self._logger = actual_get_logger(module_name)

    def info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        self._logger.info(message, extra=kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log a debug message."""
        self._logger.debug(message, extra=kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        self._logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        self._logger.error(message, extra=kwargs)


class ContextManagerAdapter(ContextManagerPort):
    """Adapter for context management."""

    def __init__(self, actual_context):
        """Initialize with the actual context manager."""
        self._context = actual_context

    def __enter__(self) -> None:
        """Enter the context."""
        self._context.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context."""
        self._context.__exit__(exc_type, exc_val, exc_tb)


class LoggingContextAdapter(LoggingContextPort):
    """Adapter for logging context."""

    def operation_context(
        self, operation_name: str, logger: LoggerPort, **context_data
    ) -> ContextManagerPort:
        """Create an operation context with the given name and context data."""
        # We know that logger is actually a LoggerAdapter instance
        internal_logger = logger._logger if hasattr(logger, "_logger") else logger
        actual_ctx = actual_operation_context(
            operation_name, internal_logger, **context_data
        )
        return ContextManagerAdapter(actual_ctx)


def get_logger(module_name: str) -> LoggerPort:
    """Get a logger adapter for the given module name."""
    return LoggerAdapter(module_name)


def get_logging_context() -> LoggingContextPort:
    """Get a logging context adapter."""
    return LoggingContextAdapter()
