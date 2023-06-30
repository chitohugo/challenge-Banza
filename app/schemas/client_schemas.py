import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, constr

from app.schemas.accounts_schemas import AccountBaseSchema
from app.schemas.category_schemas import CategoryBaseSchema


class ClientBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateClientSchema(ClientBaseSchema):
    password: constr(min_length=8)
    password_confirm: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class ClientResponseSchema(ClientBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UpdateClientSchema(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class ListClientResponseSchema(BaseModel):
    clients: List[ClientResponseSchema]


class DetailClientResponse(ClientResponseSchema):
    accounts: List[AccountBaseSchema]
    categories: List[CategoryBaseSchema]