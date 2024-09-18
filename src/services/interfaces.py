from abc import ABC, abstractmethod
from http.client import HTTPException
from typing import Dict

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.dto import UserCreate

from src.domain.auth.entities import UserBase


class AbstractUserLogin(ABC):
    username: str
    password: str


class AbstractUserRegister(AbstractUserLogin):
    email: EmailStr


class AbstractUserRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    def get_user_by(self, **filter_by) -> UserBase:
        pass

    @abstractmethod
    def update_user_by(self, filter_by: Dict, data_for_update: Dict):
        pass

    @abstractmethod
    def create_user(self, user: UserCreate) -> UserBase:
        pass

    @abstractmethod
    def delete_user(self, filter_by: Dict) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
       pass


class AbstractJWTManager(ABC):
    @staticmethod
    def encode_token(token_credentials: 'CredentialsToEncodeToken') -> str:
        pass

    @staticmethod
    def decode_token(token_credentials: 'CredentialsToDecodeToken') -> 'TokenPayload':
        pass

    @staticmethod
    def is_access_token(token_type: str) -> bool | HTTPException:
       pass

    @classmethod
    def _get_token_payload(cls, user_id: int, token_type: 'TokenType') -> 'TokenPayload':
        pass

    @classmethod
    def _get_access_token(cls, user: UserBase) -> str:
        pass

    @classmethod
    def _get_refresh_token(cls, user: UserBase) -> str:
        pass

    @staticmethod
    def create_token(user: UserBase) -> 'JWTTokens':
        pass


class AbstractPasswordManager(ABC):

    @staticmethod
    def hash_password(password: str) -> bytes:
       pass

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        pass
