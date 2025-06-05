FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Установка зависимостей
ADD . /app
WORKDIR /app
RUN uv sync --locked

# Точка входа
CMD ["fastapi", "dev", "main.py"]
