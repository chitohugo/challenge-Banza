import uuid
from typing import Dict, Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_200_OK, \
    HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST

from ..database import get_db
from ..models import Client
from ..oauth2 import require_client
from ..schemas.client_schemas import ListClientResponseSchema, ClientResponseSchema, UpdateClientSchema, \
    CreateClientSchema, DetailClientResponse
from ..utils import hash_password

router = APIRouter()


@router.post(
    '/register',
    status_code=HTTP_201_CREATED,
    response_model=ClientResponseSchema
)
def post(payload: CreateClientSchema, db: Session = Depends(get_db)):
    """
        Method that creates a client.
    Args:
        payload: dict = {
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@gmail.com",
            "password": "testing123",
            "password_confirm": "testing123"
        }
        db: Session = Session

    Returns:
        A client instance created.
        Raises 409 or 400

    """
    # Check if user already exist
    client = db.query(Client).filter_by(email=payload.email.lower()).first()

    if client:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail='Client already exist'
        )
    # Compare password and password_confirm
    if payload.password != payload.password_confirm:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Passwords do not match'
        )
    #  Hash the password
    payload.password = hash_password(payload.password)
    del payload.password_confirm

    client = Client(**payload.dict())
    db.add(client)
    db.commit()

    return client


@router.get(
    '/',
    response_model=ListClientResponseSchema,
    dependencies=[Depends(require_client)]
)
def get(db: Session = Depends(get_db)) -> Dict[str, list[Type[Client]]]:
    """
        Method that retrieves all clients.
    Args:
        db: Session = Session

    Returns:
        List of client instances
    """
    instances = db.query(Client).all()
    return {"clients": instances}


@router.get(
    '/{id}',
    status_code=HTTP_200_OK,
    response_model=DetailClientResponse,
    dependencies=[Depends(require_client)]
)
def details(id: str, db: Session = Depends(get_db)) -> Type[Client]:
    """
        Method that retrieves a client with their account details and categories
    Args:
        id: identifier of client
        db: Session = Session

    Returns:
        A client instance created with details.
        Raise 404.
    """
    client = db.query(Client) \
        .options(
        joinedload(Client.accounts),
        joinedload(Client.categories)) \
        .filter_by(id=id).first()

    if not client:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No client with this id: {id} found"
        )

    return client


@router.put(
    '/{id}',
    status_code=HTTP_200_OK,
    response_model=ClientResponseSchema
)
def update(id: str, payload: UpdateClientSchema, db: Session = Depends(get_db),
           current_client: str = Depends(require_client)) -> Type[Client]:
    """
        Method that updates client personal data.
    Args:
        id: identifier of client
        payload: dict = {
            "first_name": "New first name",
            "last_name": "New last name"
        }
        db: Session = Session
        current_client: client authenticated client

    Returns:
        A instance updated
        Raises 200 or 403

    """
    instance = db.query(Client).filter_by(id=id)

    client = instance.first()
    if not client:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No client with this id: {id} found'
        )

    if client.id == uuid.UUID(current_client):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You are not allowed to perform this action'
        )

    instance.update(payload.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return client


@router.delete(
    '/{id}',
    status_code=HTTP_204_NO_CONTENT
)
def delete(id: str, db: Session = Depends(get_db), current_client: str = Depends(require_client)) -> None:
    """
        Method that deletes a client.
    Args:
        id: identifier of client
        db: Session = Session
        current_client: client authenticated client

    Returns:
        None
        Raises 404 or 403
    """
    instance = db.query(Client).filter_by(id=id)
    client = instance.first()

    if not client:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No client with this id: {id} found'
        )

    if client.id == uuid.UUID(current_client):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action"
        )

    instance.delete(synchronize_session=False)
    db.commit()
