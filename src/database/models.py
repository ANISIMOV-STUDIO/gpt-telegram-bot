"""
Модели базы данных для хранения контекста диалогов
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_active = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связь с сообщениями
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")


class Message(Base):
    """Модель сообщения в диалоге"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    telegram_id = Column(BigInteger, nullable=False)
    role = Column(String(50), nullable=False)  # 'user' или 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    # Связь с пользователем
    user = relationship("User", back_populates="messages") 