FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml .

RUN uv pip install --system .

COPY . .

RUN chmod +x docker/api/entrypoint.sh

ENTRYPOINT ["docker/api/entrypoint.sh"]