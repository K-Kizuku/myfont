from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from schemas.fonts import FontPayload
from utils.jwt import get_current_user
from cruds.images import insert_images, delete_images_by_uid
from schemas.users import Image

font_router = APIRouter()

@font_router.post("/", response_model=list[Image])
def create_font_images(fonts_images: FontPayload, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    print(fonts_images)
    print(fonts_images == None)
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid!")
    images = insert_images(db, fonts_images.images, user_id)
    return images

@font_router.delete("/")
async def delete_font_images(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid")
    delete_images_by_uid(db, user_id)
    return {"detail" : "OK!!"}

