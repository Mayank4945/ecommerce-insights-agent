"""
Configuration module for the E-Commerce Insights Agent
Handles environment variables and application settings
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MEMORY_DIR = DATA_DIR / "memory"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


class LLMConfig(BaseModel):
    """LLM Configuration"""
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    openrouter_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY"))
    default_model: str = Field(default="gemini-2.0-flash")
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=4096)


class DatabaseConfig(BaseModel):
    """Database Configuration"""
    database_path: Path = Field(default=DATA_DIR / "ecommerce.db")
    max_query_results: int = Field(default=1000)
    query_timeout: int = Field(default=30)


class MemoryConfig(BaseModel):
    """Memory Configuration"""
    max_conversation_history: int = Field(default=20)
    enable_persistence: bool = Field(default=True)
    storage_path: Path = Field(default=MEMORY_DIR)


class APIConfig(BaseModel):
    """External API Configuration"""
    tavily_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("TAVILY_API_KEY"))
    enable_web_search: bool = Field(default=True)
    enable_translation: bool = Field(default=True)
    enable_geolocation: bool = Field(default=True)
    enable_visualizations: bool = Field(default=True)


class AppConfig(BaseModel):
    """Main Application Configuration"""
    app_name: str = Field(default="E-Commerce Insights Agent")
    debug_mode: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    llm: LLMConfig = Field(default_factory=LLMConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    api: APIConfig = Field(default_factory=APIConfig)


# Global configuration instance
config = AppConfig()


def validate_config() -> bool:
    """Validate configuration and check for required API keys"""
    if not config.llm.gemini_api_key:
        return False
    return True


def get_config() -> AppConfig:
    """Get the global configuration instance"""
    return config
