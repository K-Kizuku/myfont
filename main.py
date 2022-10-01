from fastapi import FastAPI
from db.database import engine
from db.models import Base
from schemas.schemas import EmailRequest
from utils.sendEmail import send_mail, create_message,FROM_ADDRESS
from routers.main import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="myfont_api"
)

@app.get("/")
async def myfont():
    return {"message": "welcome to myfont!"}

    
@app.post("/email")
async def send_email(address:EmailRequest):
    try:
        body = create_message(FROM_ADDRESS,address.address,"フォント作成が完了しました!","hello world")
        send_mail(FROM_ADDRESS,address.address,body)
    except:
        return {"message" : "Failed"}
    return {"message" : "Done!"}

app.include_router(router, prefix="/api/v1")