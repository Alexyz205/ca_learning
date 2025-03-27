import time
import functools
from typing import Callable, Any
from .metrics import SERVICE_OPERATIONS, SERVICE_OPERATION_LATENCY, SERVICES_COUNT
from .logging_context import get_contextual_logger

logger = get_contextual_logger(__name__)


def track_operation(operation_name: str):
    """
    Decorator to track service operations with Prometheus metrics.

    Args:
        operation_name: The name of the operation to track (e.g., "get_service", "create_service")
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                # Record success metric
                SERVICE_OPERATIONS.labels(
                    operation=operation_name, status="success"
                ).inc()

                return result
            except Exception as e:
                # Record failure metric
                SERVICE_OPERATIONS.labels(
                    operation=operation_name, status="error"
                ).inc()

                # Re-raise the exception
                raise
            finally:
                # Record operation duration
                duration = time.time() - start_time
                SERVICE_OPERATION_LATENCY.labels(operation=operation_name).observe(
                    duration
                )

        return wrapper

    return decorator


def track_async_operation(operation_name: str):
    """
    Decorator to track asynchronous service operations with Prometheus metrics.

    Args:
        operation_name: The name of the operation to track (e.g., "get_service", "create_service")
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)

                # Record success metric
                SERVICE_OPERATIONS.labels(
                    operation=operation_name, status="success"
                ).inc()

                return result
            except Exception as e:
                # Record failure metric
                SERVICE_OPERATIONS.labels(
                    operation=operation_name, status="error"
                ).inc()

                # Re-raise the exception
                raise
            finally:
                # Record operation duration
                duration = time.time() - start_time
                SERVICE_OPERATION_LATENCY.labels(operation=operation_name).observe(
                    duration
                )

        return wrapper

    return decorator
