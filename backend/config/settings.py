from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "The Linguistic Engineer"
    VERSION: str = "2.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_SECRET_KEY_12345"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database (Postgres/MySQL - Placeholder for now)
    DATABASE_URL: str = "sqlite:///./sovereign.db"
    
    # Vector DB (ChromaDB)
    CHROMA_DB_PATH: str = "./chroma_data"
    CHROMA_COLLECTION_NAME: str = "sovereign_memory"
    
    # LLM Providers (Anthropic/OpenAI/Google)
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # Model Config
    DEFAULT_MODEL: str = "claude-3-5-sonnet-20240620"
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"
    
    # Business Logic
    STRICTNESS_THRESHOLD: float = 0.95
    MAJESTY_THRESHOLD: float = 0.30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
