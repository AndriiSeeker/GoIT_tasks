from datetime import date
from pydantic import BaseModel, Field, EmailStr
from pydantic.schema import datetime


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=80)
    email: EmailStr
    phone: str = Field(max_length=100)
    birth: date = Field()
    description: str


class ContactResponse(ContactModel):
    id: int
    name: str = Field(max_length=50)
    surname: str = Field(max_length=80)
    email: EmailStr
    phone: str = Field(max_length=100)
    birth: date = Field()
    description: str

    class Config:
        orm_mode = True


...


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
