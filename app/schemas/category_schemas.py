import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class CategoryBaseSchema(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class CreateCategorySchema(BaseModel):
    name: str


class CategoryResponseSchema(CategoryBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ListCategoryResponseSchema(BaseModel):
    categories: List[CategoryResponseSchema]


class UpdateCategorySchema(BaseModel):
    name: str

    class Config:
        orm_mode = True