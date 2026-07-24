FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN python -m pip install --upgrade pip

RUN pip install \
    fastapi \
    "uvicorn[standard]" \
    sqlalchemy \
    pymysql \
    alembic \
    polars \
    python-multipart \
    pydantic \
    pydantic-settings \
    loguru \
    xlsxwriter \
    openpyxl

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]