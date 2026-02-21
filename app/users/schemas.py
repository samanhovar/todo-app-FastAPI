from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class UserLoginSchema(BaseModel):
    username: Annotated[
        str, Field(..., max_length=250, description="username of the user")
    ]
    password: Annotated[str, Field(..., description="password of the user")]


class UserRegisterSchema(BaseModel):
    username: Annotated[
        str, Field(..., max_length=250, description="username of the user")
    ]
    password: Annotated[str, Field(..., description="password of the user")]
    password_confirm: Annotated[
        str, Field(..., description="confirm password of the user")
    ]

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("passwords doesn't match")
        return password_confirm


class UserRefreshTokenSchema(BaseModel):
    token : Annotated[str, Field(..., description="refresh token of the user")]