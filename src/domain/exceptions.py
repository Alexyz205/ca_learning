class DomainException(Exception):
    """Base exception for domain errors."""
    pass

class ServiceNotFoundError(DomainException):
    """Raised when a service is not found."""
    pass

class ServiceValidationError(DomainException):
    """Raised when service validation fails."""
    pass

class ServiceAlreadyExistsError(DomainException):
    """Raised when attempting to create a duplicate service."""
    pass