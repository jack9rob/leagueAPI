from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PlayerLogin(BaseModel):
    email: EmailStr
    password: str

class PlayerCreate(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    is_admin: bool = False

class PlayerResponse(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True