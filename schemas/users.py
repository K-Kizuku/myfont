from pydantic import BaseModel, EmailStr

class SignInPayload(BaseModel):
    email: EmailStr
    password: str

class SignUpPayload(BaseModel):
    name: str
    email: EmailStr
    password: str

class Image(BaseModel):
    image_id: str
    character: str
    image_url: str

    class Config:
        orm_mode = True
    
class User(BaseModel):
    user_id: str
    name: str
    email: str
    images: list[Image]

    class Config:
        orm_mode = True


class AuthInfo(BaseModel):
    jwt: str
