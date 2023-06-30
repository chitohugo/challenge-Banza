import enum
import random
import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Enum, Float, func, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .database import Base
from .services import APIDollar, CustomRequest

response = CustomRequest.get()


def generate_account():
    _list = []
    for x in range(1, 5 + 1):
        _list.append(str(random.randint(1, 9)))

    return int("".join(_list))


class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    def __str__(self):
        return f"{self.id}"


class TypeMovements(enum.Enum):
    EGRESS = 1
    INGRESS = 2


class Client(BaseModel):
    __tablename__ = 'clients'
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    accounts = relationship('Account', backref='clients')
    categories = relationship('Category', secondary='categories_clients', backref='clients')


class Account(BaseModel):
    __tablename__ = 'accounts'
    id_client = Column(UUID(as_uuid=True), ForeignKey(
        Client.id, ondelete='CASCADE'), nullable=False)
    cod_account = Column(Integer, unique=True, nullable=False, default=generate_account)
    balance = Column(Float, nullable=False, default=0)

    @hybrid_property
    def get_total_usd(self):
        instance = APIDollar(response)
        price_dollar = instance.get_price()
        if price_dollar:
            total = self.balance / price_dollar
            return "{:.2f}".format(total)


class Category(BaseModel):
    __tablename__ = 'categories'
    name = Column(String, nullable=False)


class CategoryClient(BaseModel):
    __tablename__ = 'categories_clients'
    id_client = Column(UUID(as_uuid=True), ForeignKey(
        Client.id, ondelete='CASCADE'), nullable=False)
    id_category = Column(UUID(as_uuid=True), ForeignKey(
        Category.id, ondelete='CASCADE'), nullable=False)


class Movement(BaseModel):
    __tablename__ = 'movements'
    id_account = Column(UUID(as_uuid=True), ForeignKey(
        Account.id, ondelete='CASCADE'), nullable=False)
    type = Column(Enum(TypeMovements), nullable=False)
    amount = Column(Float, nullable=False)
