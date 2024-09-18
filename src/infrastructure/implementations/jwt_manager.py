from datetime import datetime, UTC, timedelta
from enum import Enum

import jwt
from jwt import InvalidTokenError

from fastapi import HTTPException

from src.services.interfaces import AbstractJWTManager
from src.config import settings
from src.infrastructure.dto import CredentialsToEncodeToken, CredentialsToDecodeToken, TokenPayload, JWTTokens
from src.domain.auth.entities import UserBase
from src.exceptions import get_exception_401_unauthorized_with_detail


class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTManager(AbstractJWTManager):

    @staticmethod
    def encode_token(token_credentials: CredentialsToEncodeToken) -> str:
        payload_copy = token_credentials.payload.model_copy()
        datetime_now = datetime.now(UTC)

        if token_expire_timedelta := token_credentials.expire_timedelta:
            expire = datetime_now + token_expire_timedelta
        else:
            expire = datetime_now + timedelta(minutes=token_credentials.expire_minutes)

        payload_copy.exp = expire
        payload_copy.iat = datetime_now

        encoded_jwt_token = jwt.encode(payload_copy.model_dump(), token_credentials.key,
                                       algorithm=token_credentials.algorithm)
        return encoded_jwt_token

    @staticmethod
    def decode_token(token_credentials: CredentialsToDecodeToken) -> TokenPayload:
        try:
            decoded_jwt_token = jwt.decode(token_credentials.encoded_token,
                                           token_credentials.key,
                                           algorithms=token_credentials.algorithm)
        except InvalidTokenError:
            raise get_exception_401_unauthorized_with_detail('invalid token error')
        return TokenPayload(**decoded_jwt_token)

    @staticmethod
    def is_access_token(token_type: str) -> bool | HTTPException:
        if token_type == TokenType.ACCESS.value:
            return True
        raise get_exception_401_unauthorized_with_detail('invalid token type!')

    @classmethod
    def _get_token_payload(cls, user_id: int, token_type: TokenType) -> TokenPayload:
        token_payload = TokenPayload(sub=user_id, type=token_type.value)
        return token_payload

    @classmethod
    def _get_access_token(cls, user: UserBase) -> str:
        access_token_payload = cls._get_token_payload(user.id, TokenType.ACCESS)

        token_credentials = CredentialsToEncodeToken(payload=access_token_payload,
                                                     expire_minutes=settings.authJWT.access_token_expire_minutes,
                                                     )
        access_token = cls.encode_token(token_credentials)
        return access_token

    @classmethod
    def _get_refresh_token(cls, user: UserBase):
        refresh_token_payload = cls._get_token_payload(user.id, TokenType.REFRESH)
        token_credentials = CredentialsToEncodeToken(payload=refresh_token_payload,
                                                     key=settings.authJWT.key,
                                                     expire_timedelta=timedelta(
                                                         days=settings.authJWT.refresh_token_expire_days),
                                                     )
        refresh_token = cls.encode_token(token_credentials)
        return refresh_token

    @staticmethod
    def create_token(user: UserBase) -> JWTTokens:

        access_token = JWTManager._get_access_token(user)
        refresh_token = JWTManager._get_refresh_token(user)
        token_type = settings.authJWT.token_type

        return JWTTokens(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type)
