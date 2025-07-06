"""
Управление подключением к базе данных
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from loguru import logger

from src.config import settings
from src.database.models import Base


class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
    
    async def init_db(self):
        """Инициализация базы данных"""
        try:
            # Создаем асинхронный движок
            self.engine = create_async_engine(
                settings.database_url,
                echo=False,
                poolclass=NullPool,  # Для SQLite
            )
            
            # Создаем таблицы
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            # Создаем фабрику сессий
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            logger.info("База данных успешно инициализирована")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации БД: {e}")
            raise
    
    async def close(self):
        """Закрытие соединения с БД"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Соединение с БД закрыто")
    
    @asynccontextmanager
    async def get_session(self):
        """Получение сессии для работы с БД"""
        if not self.async_session_maker:
            raise RuntimeError("База данных не инициализирована")
        
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager() 