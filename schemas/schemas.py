from pydantic import EmailStr, BaseModel

class EmailRequest(BaseModel) :
    address: EmailStr


class DeleteDetailModel(BaseModel):
    detail: str
