from dataclasses import dataclass
from typing import Annotated

from fastapi import Form
from pydantic import EmailStr

from src.services.auth.interfaces import AbstractUserLogin, AbstractUserRegister


@dataclass
class UserLoginForm(AbstractUserLogin):
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]


@dataclass
class UserRegisterForm(UserLoginForm, AbstractUserRegister):
    email: Annotated[EmailStr, Form()]
