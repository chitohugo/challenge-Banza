import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models import TypeMovements


class MovementBaseSchema(BaseModel):
    id_account: uuid.UUID
    type: TypeMovements
    amount: float

    class Config:
        orm_mode = True


class CreateMovementSchema(MovementBaseSchema):
    pass


class MovementResponseSchema(MovementBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
