from datetime import datetime, timedelta

from pydantic import EmailStr, BaseModel

from src.config import settings


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    register_at: datetime | None


class JWTTokens(BaseModel):
    access_token: bytes
    refresh_token: bytes
    token_type: str


class TokenPayload(BaseModel):
    sub: int
    type: str
    exp: datetime | None = None
    iat: datetime | None = None


class CredentialsToEncodeToken(BaseModel):
    payload: TokenPayload
    expire_minutes: int = None
    expire_timedelta: timedelta = None
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm


class CredentialsToDecodeToken(BaseModel):
    encoded_token: str
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm
