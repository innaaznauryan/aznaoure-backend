import re
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{9,15}$")

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("passwordTooShort")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("required")
        return v

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, v: str | None) -> str | None:
        if v is None or v.strip() == "":
            raise ValueError("required")
        if not PHONE_REGEX.match(v):
            raise ValueError("invalidPhone")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthRequest(BaseModel):
    credential: str

class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: str | None = None
    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
