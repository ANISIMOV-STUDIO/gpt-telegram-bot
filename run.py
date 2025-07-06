"""
Точка входа для запуска телеграм-бота
"""
import asyncio
import sys
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/bot.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG"
)


async def main():
    """Главная функция запуска бота"""
    from src.bot import bot
    
    try:
        logger.info("Запуск телеграм-бота...")
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        logger.info("Остановка бота...")
        await bot.stop()


if __name__ == "__main__":
    # Запуск асинхронной функции
    asyncio.run(main()) 