import pytest
from fastapi import HTTPException

from src.infrastructure.implementations.password_manager import PasswordManager

from tests.conftest import TestUserRegister

from src.services.auth.services import RegisterService, UserValidationService
from src.config import settings
from src.exceptions import get_exception_400_bad_request_with_detail
from src.services.auth.services import AbstractUserRepository


class TestRegister:
    def setup_method(self, method):
        self.register_data = TestUserRegister(username=settings.tests.username,
                                              password=settings.tests.password,
                                              email=settings.tests.email)

    @pytest.mark.anyio
    async def test_register(self, user_repository: AbstractUserRepository) -> None:
        register_service = RegisterService(user_repository,
                                           self.register_data,
                                           PasswordManager())
        user_validation_service = UserValidationService(user_repository)
        registered_user = await register_service.register()

        check_result = await user_validation_service.check_on_exiting_user(**registered_user.model_dump())
        assert check_result is True

        with pytest.raises(HTTPException):
            await register_service.register()
            assert get_exception_400_bad_request_with_detail

    @pytest.mark.anyio
    async def test_create_user(self, user_repository: AbstractUserRepository):
        register_service = RegisterService(user_repository,
                                           self.register_data,
                                           PasswordManager())
        created_user = await register_service.create_new_user()
        get_created_user = await user_repository.get_user_by(username=self.register_data.username,
                                                             email=self.register_data.email)
        assert created_user.username == get_created_user.username \
               and created_user.email == get_created_user.email
