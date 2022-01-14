from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}




@app.get("/posts")
def get_posts():
    return {"data": "here is your data"}