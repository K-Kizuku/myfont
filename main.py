from fastapi import FastAPI
from db.database import engine
from db.models import Base
from pydantic import EmailStr
from utils.sendEmail import send_mail, create_message,FROM_ADDRESS

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="myfont_api"
)

@app.get("/")
async def myfont():
    return {"message": "welcome to myfont!"}

    
@app.get("/email/{adress}")
async def send_email(address:EmailStr):
    body = create_message(FROM_ADDRESS,address,"フォント作成が完了しました!","hello world")
    send_mail(FROM_ADDRESS,address,body)
