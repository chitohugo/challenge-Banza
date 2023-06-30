from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.database import get_db
from app.models import Client, Category, CategoryClient
from app.oauth2 import require_client
from app.schemas.categories_clients_schemas import CreateCategoriesClientsSchema, CategoriesClientsResponseSchema

router = APIRouter()


@router.post(
    '/',
    status_code=HTTP_201_CREATED,
    response_model=CategoriesClientsResponseSchema,
    dependencies=[Depends(require_client)]
)
def post(payload: CreateCategoriesClientsSchema, db: Session = Depends(get_db)):
    """
        Method that creates a customer in category.
    Args:
        payload: {
            "id_client": identifier of client,
            "id_category": identifier of category
        }
        db: Session = Session

    Returns:
        An instance of Categories Clients
        Raises 404,
    """
    id_client = payload.id_client
    id_category = payload.id_category

    client = db.query(Client).filter_by(id=id_client).first()
    category = db.query(Category).filter_by(id=id_category).first()

    if not client:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No client with this id: {id_client} found"
        )

    if not category:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No category with this id: {id_category} found"
        )

    instance = CategoryClient(**payload.dict())
    db.add(instance)
    db.commit()

    return instance
