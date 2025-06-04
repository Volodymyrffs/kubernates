# 🚀 .NET Docker Example (DevOps Best Practices)

This is a minimal, production-ready example of containerizing a .NET console app with Docker.

## 📦 Features

- Multi-stage build for small image size  
- Uses official Microsoft .NET 8 SDK and runtime images  
- Reads sensitive data from environment variables  
- Sends a Telegram message on start

## 🛠️ Usage

### 1. Build image

```bash
docker build -t dotnet-telegram-bot .
docker run \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  dotnet-telegram-bot
