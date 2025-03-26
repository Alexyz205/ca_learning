from pathlib import Path
from typing import List
import yaml
from pydantic import ConfigDict, BaseModel

model_config = ConfigDict(
    case_sensitive=True,
    frozen=True,
    populate_by_name=True,
    str_strip_whitespace=True
)

class Settings(BaseModel):
    """Application settings."""
    
    model_config = model_config
    
    # Application settings
    app_name: str = "Clean Architecture Service"
    app_description: str = "A service implementing Clean Architecture principles"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS settings
    cors_allow_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    @classmethod
    def from_yaml(cls, config_path: Path) -> "Settings":
        """Create settings from YAML file."""
        if not config_path.exists():
            return cls()
            
        with open(config_path) as f:
            yaml_settings = yaml.safe_load(f)
            return cls(**yaml_settings if yaml_settings else {})