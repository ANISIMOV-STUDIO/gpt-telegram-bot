"""
Обработчики сообщений телеграм-бота
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

from src.config import settings
from src.services.openai_service import openai_service
from src.services.context_service import context_service


async def check_access(user_id: int) -> bool:
    """
    Проверка доступа пользователя к боту
    
    Args:
        user_id: ID пользователя в Telegram
    
    Returns:
        True если доступ разрешен
    """
    # Если список пустой - доступ для всех
    if not settings.allowed_users:
        return True
    
    return user_id in settings.allowed_users


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    if not await check_access(user.id):
        await update.message.reply_text(
            "⛔ Извините, у вас нет доступа к этому боту.\n"
            "Обратитесь к администратору для получения доступа."
        )
        return
    
    # Создаем или обновляем пользователя в БД
    await context_service.get_or_create_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот с искусственным интеллектом, который может вести диалог и помнить контекст нашего общения.\n\n"
        "Доступные команды:\n"
        "• /start - Начать работу\n"
        "• /clear - Очистить контекст диалога\n"
        "• /help - Показать помощь\n\n"
        "Просто напишите мне сообщение, и я отвечу!"
    )
    
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    if not await check_access(update.effective_user.id):
        return
    
    help_text = (
        "📚 **Помощь по использованию бота**\n\n"
        "Этот бот использует ChatGPT для генерации ответов и запоминает контекст вашего диалога.\n\n"
        "**Команды:**\n"
        "• `/start` - Начать работу с ботом\n"
        "• `/clear` - Очистить историю диалога\n"
        "• `/help` - Показать это сообщение\n\n"
        "**Особенности:**\n"
        "• Бот помнит контекст последних сообщений\n"
        "• Каждый пользователь имеет свой независимый диалог\n"
        "• История автоматически очищается через заданное время\n\n"
        "Просто отправьте любое сообщение, чтобы начать диалог!"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /clear"""
    user_id = update.effective_user.id
    
    if not await check_access(user_id):
        return
    
    # Очищаем контекст пользователя
    await context_service.clear_context(user_id)
    
    await update.message.reply_text(
        "🧹 Контекст диалога очищен.\n"
        "Начнем с чистого листа!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user = update.effective_user
    message = update.message
    
    # Проверка доступа
    if not await check_access(user.id):
        await message.reply_text(
            "⛔ У вас нет доступа к этому боту."
        )
        return
    
    # Показываем индикатор "печатает..."
    await context.bot.send_chat_action(
        chat_id=message.chat_id,
        action="typing"
    )
    
    try:
        # Создаем или обновляем пользователя
        await context_service.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Сохраняем сообщение пользователя
        await context_service.add_message(
            telegram_id=user.id,
            role="user",
            content=message.text
        )
        
        # Получаем контекст диалога
        messages = await context_service.get_context(user.id)
        
        # Добавляем системное сообщение если контекст пустой
        if not messages:
            messages.append({
                "role": "system",
                "content": "Ты дружелюбный и полезный ассистент. Отвечай на русском языке."
            })
        
        # Получаем ответ от ChatGPT
        logger.info(f"Отправка запроса к OpenAI для пользователя {user.id}")
        ai_response = await openai_service.get_chat_completion(messages)
        
        # Сохраняем ответ ассистента
        await context_service.add_message(
            telegram_id=user.id,
            role="assistant",
            content=ai_response
        )
        
        # Отправляем ответ пользователю
        await message.reply_text(ai_response)
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await message.reply_text(
            "😔 Произошла ошибка при обработке вашего сообщения.\n"
            "Попробуйте еще раз или обратитесь к администратору."
        ) 