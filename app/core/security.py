from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

RESET_TOKEN_TYPE = "password_reset"

def create_password_reset_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "type": RESET_TOKEN_TYPE, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password_reset_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != RESET_TOKEN_TYPE:
            return None
        return int(payload["sub"])
    except JWTError:
        return None