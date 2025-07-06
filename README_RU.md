# Telegram Bot с ChatGPT

Телеграм-бот с интеграцией ChatGPT, поддержкой контекста диалогов и возможностью работы через прокси.

## Возможности

- 🤖 Интеграция с ChatGPT (OpenAI API)
- 💬 Сохранение контекста диалогов для каждого пользователя
- 🔐 Ограничение доступа по списку пользователей
- 🌐 Поддержка работы через прокси (HTTP/SOCKS5)
- 📊 Автоматическая очистка старых диалогов
- 🚀 Готов к деплою на GitHub Actions

## Структура проекта

``` 
TelegramBot/
├── src/
│   ├── __init__.py
│   ├── config.py           # Конфигурация приложения
│   ├── bot.py              # Основной модуль бота
│   ├── database/           # Работа с БД
│   │   ├── models.py       # Модели данных
│   │   └── connection.py   # Управление подключением
│   ├── services/           # Бизнес-логика
│   │   ├── openai_service.py    # Работа с ChatGPT
│   │   └── context_service.py   # Управление контекстом
│   └── handlers/           # Обработчики команд
│       └── message_handler.py
├── run.py                  # Точка входа
├── requirements.txt        # Зависимости
├── env.example             # Пример конфигурации
└── .github/workflows/      # CI/CD
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ThNotorious/gpt-telegram-bot.git
cd gpt-telegram-bot
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

5. Настройте переменные окружения в `.env`:
```env
# Обязательные параметры
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_key_here

# Опциональные параметры
PROXY_URL=socks5://user:pass@host:port
ALLOWED_USERS=123456789,987654321
```

## Запуск

```bash
python run.py
```

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/clear` - Очистить контекст диалога

## Лицензия

MIT 