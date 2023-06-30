import uuid
from datetime import datetime

from pydantic import BaseModel


class CategoriesClientsSchema(BaseModel):
    id_client: uuid.UUID
    id_category: uuid.UUID

    class Config:
        orm_mode = True


class CreateCategoriesClientsSchema(CategoriesClientsSchema):
    pass


class CategoriesClientsResponseSchema(CategoriesClientsSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime