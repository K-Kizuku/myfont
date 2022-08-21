from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def myfont():
    return {"message": "welcome to myfont!"}