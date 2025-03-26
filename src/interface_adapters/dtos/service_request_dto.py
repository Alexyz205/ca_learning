from pydantic import BaseModel, Field, ConfigDict

class CreateServiceRequest(BaseModel):
    """Request model for creating a service."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the service")
    description: str = Field("", max_length=500, description="Description of the service")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "name": "Example Service",
                "description": "This is an example service.",
            }
        }