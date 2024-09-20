from datetime import datetime
from typing import Dict, Iterable

from fastapi import HTTPException

from src.db.enums import UserRole
from src.exceptions import get_exception_401_unauthorized_with_detail, get_exception_400_bad_request_with_detail

from src.services.auth.interfaces import AbstractUserRepository, AbstractUserLogin, AbstractUserRegister, AbstractPasswordManager, AbstractJWTManager
from src.domain.auth.entities import UserBase
from src.infrastructure.dto import UserCreate, JWTTokens
from src.services.auth.dto import RegisteredUser


class RegisterService:
    """ Class provides the ability to create a new user """

    def __init__(self, repository: AbstractUserRepository,
                 user_register: AbstractUserRegister,
                 password_manager: AbstractPasswordManager):
        """
            Initializes RegisterService with the given repository.
            :param repository: AbstractUserRepository, repository instance
        """
        self.repository: AbstractUserRepository = repository
        self.user_register: AbstractUserRegister = user_register
        self.password_manager: AbstractPasswordManager = password_manager

    async def register(self) -> RegisteredUser:
        """
            Method for registering new users in the system
            :return: JWTTokens, jwt token for user
        """
        new_user: UserBase = await self.create_new_user()
        registered_user: RegisteredUser = RegisteredUser(**new_user.model_dump())
        return registered_user

    async def create_new_user(self) -> UserBase:
        """
            Method for creating new user in db
            :return: UserBase, created user
        """
        await self._check_on_exiting_user()

        user: UserCreate = self._format_user_to_save()
        new_user: UserBase = await self.repository.create_user(user)
        await self.repository.commit()

        return new_user

    async def _check_on_exiting_user(self) -> bool | HTTPException:
        user_service: UserValidationService = UserValidationService(self.repository)

        if await user_service.check_on_exiting_username(self.user_register.username):
            raise get_exception_400_bad_request_with_detail('User with this username already exist!')

        if await user_service.check_on_exiting_email(self.user_register.email):
            raise get_exception_400_bad_request_with_detail('User with this email already exist!')

        return True

    def _format_user_to_save(self) -> UserCreate:
        """
            Method for formating user_register to dto instance UserCreate for further
            convenient saving to db
            :return: UserCreate, dto instance
        """
        user_data: Dict = self.user_register.__dict__
        user_hashed_password: bytes = self.password_manager.hash_password(self.user_register.password)

        user_data.update(password=user_hashed_password, register_at=datetime.now())

        user: UserCreate = UserCreate(**user_data)

        return user


class LoginService:
    """ Class provides the ability to log in user """

    def __init__(self, repository: AbstractUserRepository,
                 user_login: AbstractUserLogin,
                 jwt_manager: AbstractJWTManager,
                 password_manager: AbstractPasswordManager):
        """
            Initializes LoginService with the given repository.
            :param repository: AbstractUserRepository, repository instance
        """
        self.repository: AbstractUserRepository = repository
        self.user_login: AbstractUserLogin = user_login
        self.jwt_manager: AbstractJWTManager = jwt_manager
        self.password_manager: AbstractPasswordManager = password_manager

    async def login(self) -> JWTTokens:
        """
            Method for login users in the system
            :return: JWTTokens, jwt token for user
        """
        user: UserBase = await self.get_user()

        await self.repository.update_user_by({'id': user.id}, {'last_login': datetime.now()})
        await self.repository.commit()

        tokens: JWTTokens = self.jwt_manager.create_token(user)

        return tokens

    async def get_user(self) -> UserBase:
        """
            Method for obtain a user from the database
            :return: UserBase, user entity
        """
        user: UserBase = await self.repository.get_user_by(username=self.user_login.username)
        self.check_user_credentials(user, self.user_login.password)
        return user

    def check_user_credentials(self, user: UserBase, received_password: str) -> HTTPException | bool:
        if not user or not self.password_manager.validate_password(received_password, user.password.encode()):
            raise get_exception_401_unauthorized_with_detail('invalid username or password')
        return True


class UserValidationService:
    """
        Class for validating user credentials
    """
    def __init__(self, repository: AbstractUserRepository):
        self.repository: AbstractUserRepository = repository

    async def check_on_exiting_user(self, username: str, email: str) -> bool:
        return await self.check_on_exiting_username(username) and await self.check_on_exiting_email(email)

    async def check_on_exiting_username(self, username: str) -> bool:
        return True if await self.repository.get_user_by(username=username) else False

    async def check_on_exiting_email(self, email: str) -> bool:
        return True if await self.repository.get_user_by(email=email) else False

    @staticmethod
    def check_role_for_access_to_action(role: UserRole, available_roles: Iterable[UserRole]) -> bool:
        return role not in available_roles