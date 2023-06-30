from datetime import timedelta

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from starlette.status import HTTP_400_BAD_REQUEST

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    if not pwd_context.verify(password, hashed_password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Incorrect Email or Password'
        )
    return True


def create_access_token(client_id: str):
    authorize = AuthJWT()
    access_token = authorize.create_access_token(
        subject=client_id,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    return access_token
