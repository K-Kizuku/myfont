from pydantic import BaseModel, EmailStr

class SignInPayload(BaseModel):
    email: EmailStr
    password: str

class SignUpPayload(BaseModel):
    email: EmailStr
    password: str

class Image(BaseModel):
    image_id: str
    image_url: str

    class Config:
        orm_mode = True
    
class User(BaseModel):
    user_id: str
    email: str
    images: list[Image]

    class Config:
        orm_mode = True


class AuthInfo(BaseModel):
    jwt: str
