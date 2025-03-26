from prometheus_client import Counter, Histogram, Gauge
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# General HTTP metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests count",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["method"]
)

# Service-specific metrics
SERVICE_OPERATIONS = Counter(
    "service_operations_total",
    "Total number of service operations",
    ["operation", "status"]
)

SERVICE_OPERATION_LATENCY = Histogram(
    "service_operation_duration_seconds",
    "Duration of service operations in seconds",
    ["operation"]
)

SERVICES_COUNT = Gauge(
    "services_total",
    "Total number of services in the system"
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting Prometheus metrics."""
    
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path
        
        # Track in-progress requests
        REQUESTS_IN_PROGRESS.labels(method=method).inc()
        
        # Time the request
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            
        except Exception as e:
            status_code = 500
            raise e
        finally:
            # Record response time
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=method,
                endpoint=path
            ).observe(duration)
            
            # Count total requests
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status=status_code
            ).inc()
            
            # Track in-progress requests
            REQUESTS_IN_PROGRESS.labels(method=method).dec()
        
        return response