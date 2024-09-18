from pydantic import BaseModel, EmailStr


class RegisteredUser(BaseModel):
    username: str
    email: EmailStr
