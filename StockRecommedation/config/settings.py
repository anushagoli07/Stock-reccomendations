"""Configuration settings for the application."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    serper_api_key: str = os.getenv("SERPER_API_KEY", "")
    
    # Server Configuration
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Configuration
    # Options: "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp", "gemini-2.5-flash"
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
