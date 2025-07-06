# GPT Telegram Bot

[🇬🇧 English](README.md) • [🇷🇺 Русский](README_RU.md) • [🇨🇳 中文](README_ZH.md)

---

## Description
Telegram bot powered by OpenAI ChatGPT, supports per-user conversation context, proxy, and GitHub Actions deploy.

## Features
- 🤖 ChatGPT integration (OpenAI API)
- 💬 Context memory for every user
- 🔐 Access whitelist via `ALLOWED_USERS`
- 🌐 HTTP / SOCKS5 proxy support
- 🚀 Ready-to-use GitHub Actions workflow

## Project structure
```text
TelegramBot/
├── src/                # core code (config, bot, services)
├── run.py              # entry point
├── requirements.txt    # dependencies
├── env.example         # sample env file
└── .github/workflows/  # CI/CD
```

## Quick start
```bash
git clone https://github.com/ANISIMOV-STUDIO/gpt-telegram-bot.git
cd gpt-telegram-bot

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp env.example .env        # fill TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, etc.
python run.py
```

## Commands
- `/start` – start a new session
- `/help`  – show help
- `/clear` – clear conversation context

## License
MIT 
