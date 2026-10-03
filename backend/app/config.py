"""
Configuration settings for the Session Service.
Loads environment variables and provides application configuration.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./session_service.db"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    
    # Application Settings
    app_name: str = "SIH 26241 - Counselling Platform"
    app_version: str = "1.0.0"
    
    # Sarvam AI Configuration
    sarvam_api_key: str = ""
    
    # Groq Configuration
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3.8-27b"
    groq_model_name: str = "qwen/qwen3.8-27b"
    
    # Gemini Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"
    gemini_model_name: str = "gemini-3.1-flash-lite"
    
    # Escalation Configuration
    confidence_threshold: float = 0.7
    turn_limit: int = 5
    echo_chamber_threshold: float = 70.0
    
    # Division API Base URLs (for internal communication if deployed separately)
    division1_base_url: str = "http://localhost:8000"
    division2_base_url: str = "http://localhost:8000"
    division4_base_url: str = "http://localhost:8000"
    division5_base_url: str = "http://localhost:8000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
