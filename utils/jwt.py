from typing import Optional
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from db.models import User
from cruds.users import get_user_by_email, generate_password_hash
from sqlalchemy.orm.session import Session

SECRET = os.environ.get('SECRET', "jwt_secret")


def generate_token(db: Session, email: str, password: str) -> str:
    user: User = get_user_by_email(db, email)
    password_hash = generate_password_hash(password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail='authentication failed')

    exp_datetime = datetime.now() + timedelta(10)
    jwt_payload = {
        "exp": exp_datetime.timestamp(),
        "user_id": user.user_id
    }

    encode_jwt = jwt.encode(jwt_payload, SECRET, algorithm='HS256')

    return encode_jwt


def decode_token(token: str) -> str:
    user_dict = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = user_dict["user_id"]
    return user_id


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if credentials.scheme != 'Bearer':
            raise credentials_exception
        user_id = decode_token(credentials.credentials)
    except Exception:
        raise credentials_exception
    return user_id
