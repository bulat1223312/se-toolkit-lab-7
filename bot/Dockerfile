cat > bot/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем uv
RUN pip install uv

# Копируем файлы зависимостей
COPY pyproject.toml README.md ./

# Устанавливаем зависимости (если uv.lock нет, уберите --frozen)
RUN uv sync --frozen || uv sync

# Копируем весь код бота
COPY . .

# Запускаем бота
CMD ["uv", "run", "bot.py"]
EOF