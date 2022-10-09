from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import EmailRequest
from utils.sendEmail import send_mail, create_message, FROM_ADDRESS
from utils.jwt import get_current_user

email_router = APIRouter()

@email_router.post("/")
async def send_email(address: EmailRequest, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="jwt_token is invalid!")
    try:
        body = create_message(FROM_ADDRESS, address.address,
                              "フォント作成が完了しました!",
                              "プロトタイプなので実際に想定していた機械学習モデルのフローを追加していません。"
        )
        send_mail(FROM_ADDRESS, address.address, body)
    except:
        return {"message": "Failed"}
    return {"message": "Done!"}
