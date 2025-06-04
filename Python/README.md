# 🚀 Python Docker Example (DevOps Best Practices)

This is a minimal and production-friendly example of how to containerize a Node.js app using Docker.

## 📦 Features

- Based on `python:3.13.3-slim` for reduced image size
- Uses environment variables for API tokens
- Automatically sends a Telegram message on start

## 🛠️ Usage

### 1. Build the image

```bash
docker build -t recognition .
docker run -v "%cd%/directory:/app/directory" recognition #for CMD
docker run -v "$(pwd)/directory:/app/directory" recognition #for Linux
