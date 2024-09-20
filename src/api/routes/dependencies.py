import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.entities import UserBase
from src.exceptions import get_exception_404_not_found_with_detail
from src.infrastructure.dto import CredentialsToDecodeToken, TokenPayload
from src.infrastructure.implementations.jwt_manager import JWTManager

from src.db.database import db_helper
from src.repositories.user.repositories import UserRepository


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
oauth2_scheme = OAuth2PasswordBearer('/auth/login/')
TokenDep = Annotated[str, Depends(oauth2_scheme)]
logger = logging.getLogger('app')


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def validate_token(token: TokenDep) -> TokenPayload | HTTPException:

    token_payload: TokenPayload = JWTManager.decode_token(CredentialsToDecodeToken(encoded_token=token))
    JWTManager.is_access_token(token_payload.type)

    return token_payload


ValidateToken = Annotated[TokenPayload, Depends(validate_token)]

async def current_user(validated_token: ValidateToken, user_repository: UserRepositoryDep) -> UserBase | HTTPException:
    user_id = validated_token.sub
    logger.debug('def current_user')
    logger.debug(f'user_id = {user_id}')
    try:
        user: UserBase = await user_repository.get_user_by(id=user_id)
    except Exception as e:
        logger.error(e)
    logger.debug(f'user = {user}')

    if not user:
        return get_exception_404_not_found_with_detail('User not found')

    return user


CurrentUser = Annotated[UserBase, Depends(current_user)]
