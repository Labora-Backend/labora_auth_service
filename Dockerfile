FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/labora \
    JWT_PUBLIC_KEY_PATH=/app/jwt_keys/public.pem \
    JWT_PRIVATE_KEY_PATH=/app/jwt_keys/private.pem

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser

COPY labora_shared /opt/labora/labora_shared

COPY labora-freelancing_platform_AuthService/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY labora-freelancing_platform_AuthService/ /app/

RUN chmod +x /app/entrypoint.sh && \
    mkdir -p /app/staticfiles /app/media /app/jwt_keys && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
