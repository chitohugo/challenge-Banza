from typing import Type, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from app.database import get_db
from app.models import Account, Client
from app.oauth2 import require_client
from app.schemas.accounts_schemas import CreateAccountSchema, BalanceAccountSchema, ListAccountResponseSchema, \
    AccountResponseSchema

router = APIRouter()


@router.post(
    '/',
    status_code=HTTP_201_CREATED,
    response_model=AccountResponseSchema,
    dependencies=[Depends(require_client)]
)
def post(payload: CreateAccountSchema, db: Session = Depends(get_db)):
    """
        Method that creates an account.
    Args:
        payload: {
            "name": "name of category"
        }
        db: Session = Session

    Returns:
        A account instance created.
        Raise 404
    """
    # Check if user already exist
    client = db.query(Client).filter_by(id=payload.id_client).first()

    if not client:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No Client already exist'
        )

    account = Account(id_client=client.id)
    db.add(account)
    db.commit()

    return account


@router.get(
    "/",
    response_model=ListAccountResponseSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(require_client)],
)
def get(db: Session = Depends(get_db)) -> Dict[str, list[Type[Account]]]:
    """
         Method that retrieves all accounts.
    Args:
         db: Session = Session

    Returns:
        List of accounts instances
    """
    instances = db.query(Account).all()

    return {"accounts": instances}


@router.get(
    '/balance/',
    response_model=List[BalanceAccountSchema],
    status_code=HTTP_200_OK
)
def get(db: Session = Depends(get_db), current_client: str = Depends(require_client)) -> list[Type[Account]]:
    """
        Method that returns the balance of the accounts.
    Args:
        db: Session = Session
        current_client: client authenticated client

    Returns:
        A list with accounts and their details
        Raise 404
    """
    accounts = db.query(Account).filter_by(id_client=current_client).all()

    if not accounts:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No client with this id: {current_client} found'
        )

    return accounts
