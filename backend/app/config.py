import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    api_title: str = "GPdf API"
    api_description: str = "PDF 요약 서비스 API"
    api_version: str = "1.0.0"
    
    # Server Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # OpenAI Settings
    openai_api_key: str = ""
    
    # File Settings
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    max_pages: int = 3
    
    # Rate Limiting
    daily_limit: int = 3
    
    # CORS Settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "chrome-extension://*",
        "moz-extension://*"
    ]
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings() 