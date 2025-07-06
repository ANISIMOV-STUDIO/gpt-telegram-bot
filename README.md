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
├── env.example            # Пример конфигурации
└── .github/workflows/     # CI/CD
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/telegram-bot.git
cd telegram-bot
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

## Настройка

### Получение токена Telegram бота

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и получите токен

### Настройка прокси

Для работы через прокси укажите в `.env`:

```env
# SOCKS5 прокси
PROXY_URL=socks5://username:password@proxy.example.com:1080

# HTTP прокси
PROXY_URL=http://username:password@proxy.example.com:8080
```

### Ограничение доступа

Чтобы ограничить доступ к боту, добавьте Telegram ID пользователей:

```env
ALLOWED_USERS=123456789,987654321
```

Узнать свой Telegram ID можно у бота @userinfobot

## Запуск

```bash
python run.py
```

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/clear` - Очистить контекст диалога

## Деплой

### GitHub Actions

1. Добавьте секреты в настройках репозитория:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `OPENAI_API_BASE` (опционально)
   - `PROXY_URL` (опционально)
   - `ALLOWED_USERS` (опционально)

2. Для деплоя на сервер добавьте:
   - `SERVER_HOST`
   - `SERVER_USER`
   - `SERVER_SSH_KEY`

3. Push в ветку `main` автоматически запустит деплой

### Systemd Service (для Linux сервера)

Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot with ChatGPT
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user/telegram-bot
Environment="PATH=/home/your-user/telegram-bot/venv/bin"
ExecStart=/home/your-user/telegram-bot/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## Логирование

Логи сохраняются в папку `logs/` с ротацией по размеру (10 MB) и хранением за последние 7 дней.

## Лицензия

MIT 