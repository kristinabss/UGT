FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY pyproject.toml .
COPY README.md .

# Установка зависимостей Python
RUN pip install --no-cache-dir -e .

# Копирование исходного кода
COPY app/ ./app/

# Порт приложения
EXPOSE 8000

# Команда запуска (переопределяется в docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
