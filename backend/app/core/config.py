from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Приложение
    APP_NAME: str = "Система определения УГТ"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Сервер
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # База данных
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ugt_db"
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ML модель
    ML_MODEL_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
