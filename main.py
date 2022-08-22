from fastapi import FastAPI
from db.database import engine
from db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="myfont_api"
)

@app.get("/")
async def myfont():
    return {"message": "welcome to myfont!"}

    