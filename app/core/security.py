from datetime import datetime, timedelta, timezone
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from jose import JWTError, jwt

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_token(subject: int, token_type: str, expires_delta: timedelta) -> str:
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(subject: int) -> str:
    return create_token(
        subject,
        "access",
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(subject: int) -> str:
    return create_token(
        subject,
        "refresh",
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


class PasswordManager:
    hash = staticmethod(hash_password)
    verify = staticmethod(verify_password)


class JWTManager:
    create_access_token = staticmethod(
        lambda data: create_access_token(int(data["sub"]))
    )
    create_refresh_token = staticmethod(
        lambda data: create_refresh_token(int(data["sub"]))
    )
    decode_token = staticmethod(decode_token)


password_manager = PasswordManager()
jwt_manager = JWTManager()
