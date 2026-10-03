"""
Configuration settings for the Session Service.
Loads environment variables and provides application configuration.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./session_service.db"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Application Settings
    app_name: str = "Division 1 - Session Service"
    app_version: str = "1.0.0"
    
    # Sarvam AI Configuration
    sarvam_api_key: str = ""
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
