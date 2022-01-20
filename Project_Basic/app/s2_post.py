from email.quoprimime import body_check
from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": "here is your data"}

@app.post("/createpost")
def create_post(payload: dict = Body(...) ):
    return {"message":payload}