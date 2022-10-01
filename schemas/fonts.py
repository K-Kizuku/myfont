from pydantic import BaseModel

class FontImage(BaseModel):
    character: str
    image_url: str

class FontPayload(BaseModel):
    images: list[FontImage]

