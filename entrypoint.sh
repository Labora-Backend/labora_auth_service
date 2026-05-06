#!/bin/sh

set -e

echo "🚀 Starting Auth Service..."

# --------------------------------------------------
# Wait for DB (if using MySQL)
# --------------------------------------------------
if [ -n "$DB_HOST" ]; then
  echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
  echo "✅ MySQL is ready"
fi

# --------------------------------------------------
# Check JWT keys
# --------------------------------------------------
if [ ! -f "$JWT_PUBLIC_KEY_PATH" ]; then
  echo "❌ Public key not found at $JWT_PUBLIC_KEY_PATH"
  exit 1
fi

if [ ! -f "$JWT_PRIVATE_KEY_PATH" ]; then
  echo "❌ Private key not found at $JWT_PRIVATE_KEY_PATH"
  exit 1
fi

echo "🔐 JWT keys loaded"

# --------------------------------------------------
# Django setup
# --------------------------------------------------
echo "⚙️ Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# --------------------------------------------------
# Start server
# --------------------------------------------------
echo "🔥 Starting Django server..."

# Dev mode
python manage.py runserver 0.0.0.0:8000

# -------------------------------
# 🔴 For production (later use this)
# -------------------------------
# exec gunicorn authservice.wsgi:application --bind 0.0.0.0:8000