from datetime import timedelta, timezone, datetime

import jwt
from pwdlib import PasswordHash
from src.config import settings

class AuthService:
    password_hasher = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hasher.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        decoded_jwt = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        return decoded_jwt


