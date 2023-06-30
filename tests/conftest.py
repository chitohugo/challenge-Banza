import copy
from datetime import timedelta
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app
from app.models import Client, Category, CategoryClient, Account
from app.utils import hash_password

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test@db-test:5432/testdb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

CLIENTS = [
    {
        "first_name": "Kacie",
        "last_name": "Kalewe",
        "email": "kkalewe0@nhs.uk",
        "password": "vO1&A6x+CTek~",
        "password_confirm": "vO1&A6x+CTek~"
    },
    {
        "first_name": "Wallis",
        "last_name": "Del Dello",
        "email": "wdeldello1@nifty.com",
        "password": "pF9.n!T2<?vm",
        "password_confirm": "pF9.n!T2<?vm"
    }
]
CATEGORIES = [
    {
        "name": "Category One"
    },
    {
        "name": "Category Two"
    },
    {
        "name": "Category Three"
    }
]


@pytest.fixture(autouse=True)
def application() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = app
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(application: FastAPI) -> Generator[TestingSessionLocal, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    session = TestingSessionLocal(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def client(application: FastAPI, session: TestingSessionLocal) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def clients(session):
    clients = []
    data = copy.deepcopy(CLIENTS)

    for client in data:
        client['password'] = hash_password(client['password'])
        client.pop('password_confirm')
        instance = Client(**client)
        session.add(instance)
        session.flush()
        clients.append(instance)

    session.commit()
    yield clients


@pytest.fixture()
def token(clients):
    access_token = AuthJWT().create_access_token(
        subject=str(clients[1].id), expires_time=timedelta(minutes=60))
    yield access_token


@pytest.fixture()
def req(client, token):
    """Method with authenticated client

    Args:
        token: (JWT): Access token
        client: (TestClient):  instance of APIClient

    Returns:
        A client with authorization
    """
    client.headers = {
        "Authorization": f"Bearer {token}",
    }
    yield client


@pytest.fixture()
def categories(session):
    categories = []
    data = copy.deepcopy(CATEGORIES)

    for category in data:
        instance = Category(**category)
        session.add(instance)
        session.flush()
        categories.append(instance)

    session.commit()
    yield categories


@pytest.fixture()
def categories_clients(session, categories, clients):
    for category in categories:
        for client in clients:
            instance = CategoryClient(id_client=client.id, id_category=category.id)
            session.add(instance)
            session.flush()

    session.commit()
    yield


@pytest.fixture()
def accounts(session, clients):
    accounts = []
    for client in clients:
        instance = Account(id_client=client.id)
        session.add(instance)
        session.flush()
        accounts.append(instance)

    session.commit()
    yield accounts
