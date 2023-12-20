from datetime import datetime, timedelta

import bcrypt
import jwt

from src.core.config import settings


def encode_jwt(
        id: int,
        username: str,
        email: str,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        exp_minutes: int = settings.auth_jwt.access_token_exp_minutes
):
    jwt_payload = {
        'sub': id,
        'username': username,
        'email': email
    }

    to_encode = jwt_payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=exp_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
        token,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token, public_key, algorithms=[algorithm]
    )
    return decoded


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password,
    )
