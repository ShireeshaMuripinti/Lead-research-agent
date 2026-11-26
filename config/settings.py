"""
Configuration settings for the Lead Research Agent application.
Loads environment variables and provides configuration objects.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

class Settings:
    """Application settings loaded from environment variables."""
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./service-account-key.json")
    GOOGLE_PROJECT_ID: str = os.getenv("GOOGLE_PROJECT_ID", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Gemini Model Configuration
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2-0-flash")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    
    # Tavily API Configuration
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    MAX_TAVILY_RESULTS: int = int(os.getenv("MAX_TAVILY_RESULTS", "5"))
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./database/lra_research.db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database/lra_research.db")
    
    # Logging Configuration
    LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Lead Research Agent")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Research Configuration
    MAX_TAVILY_RESULTS: int = int(os.getenv("MAX_TAVILY_RESULTS", "10"))
    RESEARCH_TIMEOUT: int = int(os.getenv("RESEARCH_TIMEOUT", "300"))
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT: int = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are present."""
        required_settings = [
            "TAVILY_API_KEY",
            "GOOGLE_PROJECT_ID",
        ]
        
        missing = []
        for setting in required_settings:
            if not getattr(cls, setting):
                missing.append(setting)
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

settings = Settings()
