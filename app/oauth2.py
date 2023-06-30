from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import Client


class Settings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()



class ClientNotFound(Exception):
    pass


def require_client(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_client = Authorize.get_jwt_subject()
        client = db.query(Client).filter_by(id=current_client).first()

        if not client:
            raise ClientNotFound('Client no longer exist')

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'ClientNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Client no longer exist')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return current_client
