"""
Сервис управления контекстом диалогов
"""
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from loguru import logger

from src.config import settings
from src.database.connection import db_manager
from src.database.models import User, Message


class ContextService:
    """Сервис для управления контекстом диалогов пользователей"""
    
    async def get_or_create_user(self, telegram_id: int, **user_data) -> User:
        """
        Получение или создание пользователя
        
        Args:
            telegram_id: ID пользователя в Telegram
            **user_data: Дополнительные данные пользователя
        
        Returns:
            Объект пользователя
        """
        async with db_manager.get_session() as session:
            # Ищем существующего пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Создаем нового пользователя
                user = User(
                    telegram_id=telegram_id,
                    username=user_data.get('username'),
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name')
                )
                session.add(user)
                await session.commit()
                logger.info(f"Создан новый пользователь: {telegram_id}")
            else:
                # Обновляем время последней активности
                user.last_active = datetime.utcnow()
                await session.commit()
            
            return user
    
    async def add_message(
        self,
        telegram_id: int,
        role: str,
        content: str
    ) -> None:
        """
        Добавление сообщения в контекст
        
        Args:
            telegram_id: ID пользователя в Telegram
            role: Роль отправителя ('user' или 'assistant')
            content: Текст сообщения
        """
        async with db_manager.get_session() as session:
            # Получаем пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                logger.error(f"Пользователь {telegram_id} не найден")
                return
            
            # Создаем сообщение
            message = Message(
                user_id=user.id,
                telegram_id=telegram_id,
                role=role,
                content=content
            )
            session.add(message)
            await session.commit()
            
            logger.debug(f"Добавлено сообщение от {role} для пользователя {telegram_id}")
    
    async def get_context(self, telegram_id: int) -> List[Dict[str, str]]:
        """
        Получение контекста диалога пользователя
        
        Args:
            telegram_id: ID пользователя в Telegram
        
        Returns:
            Список сообщений в формате для OpenAI API
        """
        async with db_manager.get_session() as session:
            # Получаем последние сообщения пользователя
            result = await session.execute(
                select(Message)
                .where(Message.telegram_id == telegram_id)
                .order_by(Message.created_at.desc())
                .limit(settings.max_context_messages)
            )
            messages = result.scalars().all()
            
            # Преобразуем в формат OpenAI и разворачиваем в правильном порядке
            context = [
                {"role": msg.role, "content": msg.content}
                for msg in reversed(messages)
            ]
            
            logger.debug(f"Загружен контекст для пользователя {telegram_id}: {len(context)} сообщений")
            return context
    
    async def clear_context(self, telegram_id: int) -> None:
        """
        Очистка контекста диалога пользователя
        
        Args:
            telegram_id: ID пользователя в Telegram
        """
        async with db_manager.get_session() as session:
            await session.execute(
                delete(Message).where(Message.telegram_id == telegram_id)
            )
            await session.commit()
            logger.info(f"Контекст пользователя {telegram_id} очищен")
    
    async def cleanup_old_contexts(self) -> None:
        """Очистка устаревших контекстов"""
        cutoff_date = datetime.utcnow() - timedelta(hours=settings.context_ttl_hours)
        
        async with db_manager.get_session() as session:
            result = await session.execute(
                delete(Message).where(Message.created_at < cutoff_date)
            )
            await session.commit()
            
            if result.rowcount > 0:
                logger.info(f"Удалено {result.rowcount} устаревших сообщений")


# Глобальный экземпляр сервиса
context_service = ContextService() 