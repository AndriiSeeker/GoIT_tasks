from datetime import date
from pydantic import BaseModel, Field, EmailStr


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
