from functools import wraps
from typing import Any, Callable, TypeVar
from fastapi import Request
from .logging_context import request_id

T = TypeVar("T")


def with_logging_context(dependency: Callable[..., T]) -> Callable[..., T]:
    """Decorator to ensure logging context is maintained in FastAPI dependencies."""

    @wraps(dependency)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        # Extract request from args or kwargs
        request = next(
            (arg for arg in args if isinstance(arg, Request)),
            kwargs.get("request", None),
        )

        # Set request ID in context if available
        if request and hasattr(request.state, "request_id"):
            request_id.set(request.state.request_id)

        try:
            # Call the original dependency
            return await dependency(*args, **kwargs)
        finally:
            # Clean up context
            request_id.set(None)

    return wrapper
