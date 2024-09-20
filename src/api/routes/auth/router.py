import logging

from fastapi import APIRouter

from src.infrastructure.implementations.jwt_manager import JWTManager
from src.infrastructure.implementations.password_manager import PasswordManager
from .dependencies import UserRegisterFormDep, UserLoginFormDep
from src.services.auth.services import RegisterService, LoginService
from src.services.auth.dto import RegisteredUser
from src.infrastructure.dto import JWTTokens

from src.api.routes.dependencies import UserRepositoryDep


auth = APIRouter(prefix='/auth')
logger = logging.getLogger('app')


@auth.post('/register/', response_model=RegisteredUser)
async def register_user(user_repository: UserRepositoryDep, user_register_form: UserRegisterFormDep) -> RegisteredUser:
    logger.debug('def register_user')
    logger.debug(f'user_register_form = {user_register_form}')

    register_service: RegisterService = RegisterService(user_repository,
                                                        user_register_form,
                                                        PasswordManager()
                                                        )
    registered_user: RegisteredUser = await register_service.register()

    logger.debug(f'registered_user = {registered_user}')
    return registered_user

@auth.post('/login/', response_model=JWTTokens)
async def auth_user(user_repository: UserRepositoryDep, user_login_form: UserLoginFormDep) -> JWTTokens:
    logger.debug('def auth_user')
    logger.debug(f'user_login_form = {user_login_form}')

    login_service: LoginService = LoginService(user_repository,
                                               user_login_form,
                                               JWTManager(), PasswordManager())
    tokens: JWTTokens = await login_service.login()

    logger.debug(f'token value = {tokens.__dict__}')
    return tokens
