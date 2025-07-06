"""
Сервис для работы с OpenAI API
"""
from typing import List, Dict, Optional
import httpx
from httpx_socks import AsyncProxyTransport
from openai import AsyncOpenAI
from loguru import logger

from src.config import settings


class OpenAIService:
    """Сервис для взаимодействия с ChatGPT через API"""
    
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Инициализация клиента OpenAI с поддержкой прокси"""
        http_client = None
        
        # Настройка прокси если указан
        if settings.proxy_url:
            logger.info(f"Используется прокси: {settings.proxy_url}")
            
            # Определяем тип прокси
            if settings.proxy_url.startswith("socks"):
                transport = AsyncProxyTransport.from_url(settings.proxy_url)
                http_client = httpx.AsyncClient(transport=transport)
            else:
                # HTTP/HTTPS прокси
                http_client = httpx.AsyncClient(proxies=settings.proxy_url)
        
        # Создаем клиент OpenAI
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
            http_client=http_client
        )
        
        logger.info("OpenAI клиент инициализирован")
    
    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Получение ответа от ChatGPT
        
        Args:
            messages: История сообщений в формате OpenAI
            temperature: Температура генерации (0-2)
            max_tokens: Максимальное количество токенов в ответе
        
        Returns:
            Текст ответа от модели
        """
        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка при обращении к OpenAI API: {e}")
            raise
    
    async def close(self):
        """Закрытие HTTP клиента"""
        if self.client and self.client._client:
            await self.client._client.aclose()


# Глобальный экземпляр сервиса
openai_service = OpenAIService() 