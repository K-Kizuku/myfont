import bcrypt
import os
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from db.models import User
from schemas.users import User as UserSchema


salt = os.environ.get("PASSWORD_HASH_SALT",
                      "$2a$12$4CZUCt6WH8ftjjlKsASceu").encode()


def generate_password_hash(password: str):
    hash = bcrypt.hashpw(password.encode(), salt)
    return hash.decode()


def create_user(db: Session,email: str, password: str) -> UserSchema:
    same_user = db.query(User).filter(User.email == email).first()
    if same_user is not None:
        raise HTTPException(
            status_code=400, detail="User is already existed!!")
    password_hash = generate_password_hash(password)
    user_orm = User(
        email=email,
        password_hash=password_hash
    )
    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    user = UserSchema.from_orm(user_orm)
    return user


def get_user_by_id(db: Session, user_id: str) -> UserSchema:
    user_orm = db.query(User).filter(User.user_id == user_id).first()
    if user_orm is None:
        raise HTTPException(status_code=400, detail="user not exist")
    user = UserSchema.from_orm(user_orm)
    return user


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="user not exist")
    return user


def delete_user_by_id(db: Session, user_id: str) -> None:
    user_orm = db.query(User).filter(User.user_id == user_id).first()
    if user_orm is None:
        raise HTTPException(status_code=400, detail="user not exist")
    db.delete(user_orm)
    db.commit()
    return
