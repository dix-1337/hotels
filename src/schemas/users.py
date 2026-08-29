from fastapi import HTTPException

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from sqlalchemy import String


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str