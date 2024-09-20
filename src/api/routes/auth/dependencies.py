from typing import Annotated

from fastapi import Depends

from src.services.auth.interfaces import AbstractUserLogin, AbstractUserRegister
from src.api.routes.auth.dto import UserLoginForm, UserRegisterForm

UserLoginFormDep = Annotated[AbstractUserLogin, Depends(UserLoginForm)]
UserRegisterFormDep = Annotated[AbstractUserRegister, Depends(UserRegisterForm)]
