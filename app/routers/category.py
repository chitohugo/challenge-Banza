from typing import Dict, Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from app.database import get_db
from app.models import Category
from app.oauth2 import require_client
from app.schemas.category_schemas import CreateCategorySchema, ListCategoryResponseSchema, CategoryResponseSchema, \
    UpdateCategorySchema

router = APIRouter()


@router.post(
    '/',
    status_code=HTTP_201_CREATED,
    response_model=CategoryResponseSchema,
    dependencies=[Depends(require_client)]
)
def post(payload: CreateCategorySchema, db: Session = Depends(get_db)):
    """
       Method that creates a category.
    Args:
        payload: {
            "name": "name of category"
        }
        db: Session = Session

    Returns:
         A category instance created.
    """
    category = Category(**payload.dict())
    db.add(category)
    db.commit()

    return category


@router.get(
    '/',
    status_code=HTTP_200_OK,
    response_model=ListCategoryResponseSchema,
    dependencies=[Depends(require_client)]
)
def get(db: Session = Depends(get_db)) -> Dict[str, list[Type[Category]]]:
    """
        Method that retrieves all categories.
    Args:
        db: Session = Session

    Returns:
        List of categories instances
    """
    instances = db.query(Category).all()
    return {"categories": instances}


@router.get(
    '/{id}',
    status_code=HTTP_200_OK,
    response_model=CategoryResponseSchema,
    dependencies=[Depends(require_client)]
)
def retrieve(id: str, db: Session = Depends(get_db)) -> Type[Category]:
    """
        Method that retrieve a category with details
    Args:
        id: identifier of category
        db: Session = Session

    Returns:
        A category instance created with details.
        Raise 404.
    """
    category = db.query(Category).filter_by(id=id).first()
    if not category:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No category with this id: {id} found")
    return category


@router.put(
    '/{id}',
    status_code=HTTP_200_OK,
    response_model=CategoryResponseSchema,
    dependencies=[Depends(require_client)]
)
def update(id: str, payload: UpdateCategorySchema, db: Session = Depends(get_db)) -> Type[Category]:
    """
        Method that updates category.
    Args:
        id: identifier of category
        payload: dict = {
            "name": "New name",
        }
        db: Session = Session

    Returns:
        A instance updated
        Raises 404
    """
    instance = db.query(Category).filter_by(id=id)
    category = instance.first()
    if not category:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No category with this id: {id} found'
        )

    instance.update(payload.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return category


@router.delete(
    '/{id}',
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_client)]
)
def delete(id: str, db: Session = Depends(get_db)) -> None:
    """
        Method that deletes a category.
    Args:
        id: identifier of category
        db: Session = Session

    Returns:
        None
        Raise 404
    """
    instance = db.query(Category).filter_by(id=id)
    category = instance.first()

    if not category:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'No category with this id: {id} found'
        )

    instance.delete(synchronize_session=False)
    db.commit()
