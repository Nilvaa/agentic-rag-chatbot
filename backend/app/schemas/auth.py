import re
from pydantic import BaseModel,EmailStr,field_validator

PASSWORD_REGEX = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

class RegisterRequest(BaseModel):
    email:EmailStr
    password:str

    @field_validator("password")
    @classmethod
    def validate_password(cls,password:str):
        if not re.match(PASSWORD_REGEX,password):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number, and one special character."
            )

        return password

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str