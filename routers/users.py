from db.database import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from schemas.schemas import DeleteDetailModel
from schemas.users import User as UserSchema
from schemas.users import SignUpPayload, SignInPayload, AuthInfo
from db.database import get_db
from cruds.users import create_user, get_user_by_id, delete_user_by_id
from utils.jwt import generate_token, get_current_user

user_router = APIRouter()


@user_router.post("/signup", response_model=UserSchema)
async def signup(payload: SignUpPayload, db: Session = Depends(get_db)):
    user = create_user(db, payload.email, payload.password)
    return user


@user_router.post("/signin", response_model=AuthInfo)
async def signin(payload: SignInPayload, db: Session = Depends(get_db)):
    auth_info = {"jwt": generate_token(db, payload.email, payload.password)}
    return auth_info


@user_router.get('/me', response_model=UserSchema)
async def get_me(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid")
    user = get_user_by_id(db, user_id)
    return user


@user_router.delete('/me', response_model=DeleteDetailModel)
async def delete_user(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid!")
    delete_user_by_id(db, user_id)
    return {'detail': 'OK'}


@user_router.get("/{uid}", response_model=UserSchema)
async def get_user(uid: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid!")
    user = get_user_by_id(db, uid)
    return user
