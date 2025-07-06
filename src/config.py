"""
Конфигурация приложения с валидацией через Pydantic
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения"""
    
    # Telegram
    telegram_bot_token: str = Field(..., description="Токен телеграм-бота")
    
    # OpenAI
    openai_api_key: str = Field(..., description="API ключ OpenAI")
    openai_api_base: str = Field(
        default="https://api.openai.com/v1",
        description="Базовый URL для OpenAI API"
    )
    openai_model: str = Field(
        default="gpt-3.5-turbo",
        description="Модель OpenAI для использования"
    )
    
    # Прокси
    proxy_url: Optional[str] = Field(None, description="URL прокси-сервера")
    
    # Безопасность
    allowed_users: List[int] = Field(
        default_factory=list,
        description="Список разрешенных пользователей"
    )
    
    # База данных
    database_url: str = Field(
        default="sqlite+aiosqlite:///./bot_database.db",
        description="URL подключения к БД"
    )
    
    # Логирование
    log_level: str = Field(default="INFO", description="Уровень логирования")
    
    # Контекст
    max_context_messages: int = Field(
        default=20,
        description="Максимальное количество сообщений в контексте"
    )
    context_ttl_hours: int = Field(
        default=24,
        description="Время жизни контекста в часах"
    )
    
    @validator("allowed_users", pre=True)
    def parse_allowed_users(cls, v):
        """Парсинг списка пользователей из строки"""
        if isinstance(v, str):
            return [int(user_id.strip()) for user_id in v.split(",") if user_id.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings() 