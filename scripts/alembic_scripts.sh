#!/bin/bash

# Wait for Postgres to be ready
echo "Waiting for postgres at db:5432..."
# while ! nc -z db 5432; do
while ! python -c "import socket; s = socket.socket(); s.connect(('db', 5432))" > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is up and running!"

# Run Migrations
# DATABASE_URL_AlEMBIC must be in .env
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI server
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
