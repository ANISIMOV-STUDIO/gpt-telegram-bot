"""
Основной модуль телеграм-бота
"""
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from loguru import logger

from src.config import settings
from src.database.connection import db_manager
from src.services.context_service import context_service
from src.handlers.message_handler import (
    start_command,
    help_command,
    clear_command,
    handle_message
)


class TelegramBot:
    """Основной класс телеграм-бота"""
    
    def __init__(self):
        self.application = None
    
    async def initialize(self):
        """Инициализация бота и всех сервисов"""
        # Инициализируем базу данных
        await db_manager.init_db()
        
        # Создаем приложение
        self.application = (
            Application.builder()
            .token(settings.telegram_bot_token)
            .build()
        )
        
        # Регистрируем обработчики
        self._register_handlers()
        
        # Запускаем периодическую очистку контекстов
        asyncio.create_task(self._periodic_cleanup())
        
        logger.info("Бот инициализирован")
    
    def _register_handlers(self):
        """Регистрация обработчиков команд и сообщений"""
        # Команды
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("clear", clear_command))
        
        # Текстовые сообщения
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )
        
        logger.info("Обработчики зарегистрированы")
    
    async def _periodic_cleanup(self):
        """Периодическая очистка устаревших контекстов"""
        while True:
            try:
                await asyncio.sleep(3600)  # Каждый час
                await context_service.cleanup_old_contexts()
            except Exception as e:
                logger.error(f"Ошибка при очистке контекстов: {e}")
    
    async def start(self):
        """Запуск бота"""
        await self.initialize()
        
        # Запускаем polling
        logger.info("Запуск бота...")
        await self.application.run_polling(drop_pending_updates=True)
    
    async def stop(self):
        """Остановка бота"""
        if self.application:
            await self.application.stop()
        
        # Закрываем соединения
        await db_manager.close()
        
        # Закрываем OpenAI клиент
        from src.services.openai_service import openai_service
        await openai_service.close()
        
        logger.info("Бот остановлен")


# Глобальный экземпляр бота
bot = TelegramBot() 