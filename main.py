from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def myfont():
    return {"message": "welcome to myfont!"}

@app.get("/{id}")
async def get_id(id:str):
    return {"message": id}
    