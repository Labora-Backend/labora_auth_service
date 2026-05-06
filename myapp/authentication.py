from datetime import datetime, timedelta, timezone
import uuid

import jwt
from django.conf import settings


def _encode_token(payload):
    return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")


def generate_tokens(user):
    now = datetime.now(timezone.utc)
    access_payload = {
        "token_type": "access",
        "user_id": user.id,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_MINUTES),
    }
    refresh_payload = {
        "token_type": "refresh",
        "user_id": user.id,
        "role": user.role,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + timedelta(days=settings.JWT_REFRESH_TOKEN_DAYS),
    }

    return {
        "access": _encode_token(access_payload),
        "refresh": _encode_token(refresh_payload),
    }