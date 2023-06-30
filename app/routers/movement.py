from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_200_OK

from app.database import get_db
from app.models import Movement, Account, TypeMovements
from app.oauth2 import require_client
from app.schemas.movements_schemas import CreateMovementSchema, MovementResponseSchema

router = APIRouter()


@router.get(
    '/{id}',
    status_code=HTTP_200_OK,
    response_model=MovementResponseSchema,
    dependencies=[Depends(require_client)]
)
def get(id: str, db: Session = Depends(get_db)) -> Type[Movement] | None:
    """
        Method that retrieves a movement
    Args:
        id: identifier of movement
        db: Session = Session

    Returns:
       A movement instance created with details.
    """
    instance = db.query(Movement).filter_by(id=id).first()
    return instance


@router.post(
    '/',
    status_code=HTTP_201_CREATED,
    response_model=MovementResponseSchema,
    dependencies=[Depends(require_client)]
)
def post(payload: CreateMovementSchema, db: Session = Depends(get_db)):
    """
        Method that creates a movement.
    Args:
        payload: {
            "id_account": identifier of account,
            "amount": "amount",
            "type": 1 or 2
        }
        db: Session = Session

    Returns:
        A movement instance created.
        Raises 404 or 400
    """
    id_account = payload.id_account
    amount = payload.amount

    instance = db.query(Account).filter_by(id=id_account)
    account = instance.first()

    if not account:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No account with this id: {id_account} found'
        )

    if payload.type.value == TypeMovements.EGRESS.value:
        if account.balance < amount:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="You don't have enough balance"
            )
        else:
            balance = account.balance - amount

    else:
        balance = account.balance + amount

    movement = Movement(**payload.dict())
    db.add(movement)

    instance.update({"balance": balance}, synchronize_session=False)
    db.commit()

    return movement


@router.delete(
    '/{id}',
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_client)],
)
def delete(id: str, db: Session = Depends(get_db)) -> None:
    """
        Method that deletes a movement. canceling operation in the account.
    Args:
        id: identifier of movement
        ddb: Session = Session

    Returns:
        None
        Raises 404
    """
    instance = db.query(Movement).filter_by(id=id)

    movement = instance.first()
    if not movement:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No movement with this id: {id} found'
        )

    instance_account = db.query(Account).filter_by(id=movement.id_account)
    account = instance_account.first()

    if not account:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No account with this id: {movement.id_account} found'
        )

    if movement.type.value == TypeMovements.EGRESS.value:
        balance = account.balance + movement.amount

    else:
        balance = account.balance - movement.amount

    instance_account.update({"balance": balance}, synchronize_session=False)
    instance.delete(synchronize_session=False)
    db.commit()
