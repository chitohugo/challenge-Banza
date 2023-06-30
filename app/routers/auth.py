from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.oauth2 import AuthJWT
from ..config import settings
from ..database import get_db
from ..models import Client
from ..schemas.client_schemas import LoginSchema
from ..utils import verify_password, create_access_token

router = APIRouter()


@router.post('/login')
def login(payload: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
        Method for authentication
    Args:
        payload: {
            "email": "test@gmail.com",
            "password": "testing123"
        }
        db: Session = Session
        Authorize: AuthJWT = AuthJWT

    Returns:
        A token with access
        Raises 400,
    """
    # Check if the user exist
    client = db.query(Client).filter_by(email=payload.email.lower()).first()

    if not client:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Check if the password is valid
    verify_password(payload.password, client.password)

    # Create access token
    access_token = create_access_token(str(client.id))

    # Send both access
    return {'status': 'success', 'access_token': access_token}
