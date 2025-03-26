import logging
import time
from contextlib import contextmanager
from typing import Optional, Dict, Any
from contextvars import ContextVar

# Context variables for request tracking
request_id: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
operation_id: ContextVar[Optional[str]] = ContextVar('operation_id', default=None)

class ContextualLogger:
    """Logger that includes context information in all log messages."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    
    def _add_context(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add context information to log extras."""
        ctx = {}
        
        # Add request context if available
        req_id = request_id.get()
        if req_id:
            ctx['request_id'] = req_id
            
        # Add operation context if available
        op_id = operation_id.get()
        if op_id:
            ctx['operation_id'] = op_id
            
        # Add any extra context, avoiding reserved names
        if extra:
            # Map reserved names to alternatives
            name_mapping = {
                'message': 'log_message',
                'name': 'entity_name',
                'asctime': 'event_time'
            }
            for key, value in extra.items():
                safe_key = name_mapping.get(key, key)
                ctx[safe_key] = value
            
        return ctx

    def debug(self, msg: str, *args, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self._logger.debug(msg, *args, extra=self._add_context(extra), **kwargs)

    def info(self, msg: str, *args, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self._logger.info(msg, *args, extra=self._add_context(extra), **kwargs)

    def warning(self, msg: str, *args, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self._logger.warning(msg, *args, extra=self._add_context(extra), **kwargs)

    def error(self, msg: str, *args, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self._logger.error(msg, *args, extra=self._add_context(extra), **kwargs)

@contextmanager
def operation_context(name: str, logger: Optional[ContextualLogger] = None, **context):
    """Context manager for tracking operations with timing and structured logging."""
    start_time = time.time()
    op_id = f"{name}_{int(start_time * 1000)}"
    operation_id.set(op_id)
    
    try:
        if logger:
            logger.info(f"Starting operation: {name}", extra={
                "operation": name,
                "operation_id": op_id,
                **context
            })
        
        yield
        
    except Exception as e:
        if logger:
            logger.error(f"Operation failed: {name}", extra={
                "operation": name,
                "operation_id": op_id,
                "error_details": str(e),
                "duration_ms": int((time.time() - start_time) * 1000),
                **context
            })
        raise
        
    else:
        if logger:
            logger.info(f"Operation completed: {name}", extra={
                "operation": name,
                "operation_id": op_id,
                "duration_ms": int((time.time() - start_time) * 1000),
                **context
            })
    
    finally:
        operation_id.set(None)

def get_contextual_logger(name: str) -> ContextualLogger:
    """Get a contextual logger instance."""
    return ContextualLogger(logging.getLogger(name))