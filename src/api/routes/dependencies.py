from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.dto import CredentialsToDecodeToken, TokenPayload
from src.infrastructure.implementations.jwt_manager import JWTManager

from src.db.database import db_helper
from src.repositories.user.repositories import UserRepository


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
oauth2_scheme = OAuth2PasswordBearer('/auth/login/')
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def validate_token(token: TokenDep) -> TokenPayload | HTTPException:
    token_payload = JWTManager.decode_token(CredentialsToDecodeToken(encode_token=token))
    JWTManager.is_access_token(token_payload.type)
    return token_payload


ValidateToken = Annotated[TokenPayload, Depends(validate_token)]
