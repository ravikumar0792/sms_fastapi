from pydantic import BaseModel, EmailStr, field_validator
import re

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    password: str
    role_id: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase letter")
        return v


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class AdminCreateUser(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    password: str
    role: str