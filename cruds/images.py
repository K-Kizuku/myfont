from sqlalchemy.orm import Session
from db.models import Image
from schemas.users import Image as ImageSchema
from schemas.fonts import FontImage
from utils.fileUploader import getClondinaryUrl, deleteImage

def insert_images(db: Session, images: list[FontImage], user_id) -> list[ImageSchema]:
    for image in images:
        result_url = getClondinaryUrl(image.character ,image.image_url, user_id)
        image_orm = Image(
            character=image.character,
            image_url=result_url,
            user_id=user_id,
        )
        db.add(image_orm)
        db.commit()
    user_image_orm = db.query(Image).filter(Image.user_id == user_id).all()
    user_image = list(map(ImageSchema.from_orm,user_image_orm))
    return user_image

def delete_images_by_uid(db: Session, user_id) -> None:
    user_images = db.query(Image).filter(Image.user_id == user_id).all()
    for image in user_images:
        db.delete(image)
        db.commit()
    deleteImage(user_id)
    return {"detail" : "OK!!"}