FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN pip install \
    fastapi==0.116.0 \
    "uvicorn[standard]==0.35.0" \
    sqlalchemy==2.0.41 \
    pymysql==1.1.1 \
    alembic==1.16.4 \
    polars==1.31.0 \
    python-multipart==0.0.20 \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    loguru==0.7.3 \
    xlsxwriter==3.2.5 \
    openpyxl==3.1.5 \
    passlib==1.7.4 \
    bcrypt==4.0.1 \
    "python-jose[cryptography]==3.5.0"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]