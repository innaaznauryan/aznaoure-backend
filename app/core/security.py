from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

RESET_TOKEN_TYPE = "password_reset"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"type": ACCESS_TOKEN_TYPE, "exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "type": REFRESH_TOKEN_TYPE, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type", ACCESS_TOKEN_TYPE) != ACCESS_TOKEN_TYPE:
            return None
        return payload
    except JWTError:
        return None

def verify_refresh_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != REFRESH_TOKEN_TYPE:
            return None
        return int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        return None

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