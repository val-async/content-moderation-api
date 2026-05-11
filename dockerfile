FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

COPY requirements-heavy.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements-heavy.txt

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# runtime libs 
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

#copy from builder
COPY --from=builder /install /usr/local

COPY . .

COPY scripts/alembic_scripts.sh /alembic_scripts.sh
RUN chmod +x /alembic_scripts.sh

EXPOSE 8000

CMD ["/alembic_scripts.sh"]
