import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class AccountBaseSchema(BaseModel):
    id: uuid.UUID
    cod_account: int = None

    class Config:
        orm_mode = True


class CreateAccountSchema(BaseModel):
    id_client: uuid.UUID


class BalanceAccountSchema(AccountBaseSchema):
    balance: float = None
    get_total_usd: float | None = None


class ListAccountResponseSchema(BaseModel):
    accounts: List[AccountBaseSchema]


class AccountResponseSchema(AccountBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime