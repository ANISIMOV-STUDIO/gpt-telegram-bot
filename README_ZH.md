# GPT Telegram 机器人

基于 ChatGPT 的 Telegram 机器人，支持多用户对话上下文和代理。

## 功能

- 🤖 集成 OpenAI ChatGPT API
- 💬 为每个用户保存最近对话上下文
- 🔐 可通过 `ALLOWED_USERS` 限制访问
- 🌐 支持 HTTP/SOCKS5 代理
- 🚀 GitHub Actions 可自动部署

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/ThNotorious/gpt-telegram-bot.git
cd gpt-telegram-bot

# 依赖
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt

# 环境变量
cp env.example .env   # 编辑 .env 填入 TELEGRAM_BOT_TOKEN、OPENAI_API_KEY 等

# 运行
python run.py
```

## 主要命令

- `/start` 开始
- `/help` 帮助
- `/clear` 清空对话

## 许可证

MIT 