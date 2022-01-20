from email.quoprimime import body_check
from turtle import title
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": "here is your data"}

@app.post("/createpost")
def create_post(post: Post):
    post.dict()
    return {"message": post}