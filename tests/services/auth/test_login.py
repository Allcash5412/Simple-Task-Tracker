import pytest

from fastapi import HTTPException

from tests.conftest import TestUser

from src.services.interfaces import AbstractUserRepository
from src.services.auth import LoginService

from src.domain.auth.entities import UserBase

from src.infrastructure.implementations.jwt_manager import JWTManager
from src.infrastructure.implementations.password_manager import PasswordManager
from src.infrastructure.dto import JWTTokens

from src.exceptions import get_exception_401_unauthorized_with_detail


class TestLogin:

    @pytest.mark.anyio
    async def test_login(self, user_repository: AbstractUserRepository, exist_user: TestUser,
                         non_exist_user: TestUser) -> None:
        login_service = LoginService(user_repository, exist_user, JWTManager(),
                                     PasswordManager())

        tokens: JWTTokens = await login_service.login()

        assert type(tokens) is JWTTokens
        assert (tokens.access_token and tokens.refresh_token) is not None

        with pytest.raises(HTTPException):
            login_service = LoginService(user_repository, non_exist_user, JWTManager(),
                                         PasswordManager())
            await login_service.login()
            assert get_exception_401_unauthorized_with_detail

    @pytest.mark.anyio
    async def test_get_user(self, user_repository: AbstractUserRepository, exist_user: TestUser,
                            non_exist_user: TestUser) -> None:
        login_service = LoginService(user_repository, exist_user, JWTManager(),
                                     PasswordManager())
        user: UserBase = await login_service.get_user()

        assert type(user) is UserBase
        assert (user.username == exist_user.username and
                PasswordManager.validate_password(exist_user.password,
                                                  user.password.encode()))

        with pytest.raises(HTTPException):
            login_service = LoginService(user_repository, non_exist_user, JWTManager(),
                                         PasswordManager())
            await login_service.get_user()
            assert get_exception_401_unauthorized_with_detail
