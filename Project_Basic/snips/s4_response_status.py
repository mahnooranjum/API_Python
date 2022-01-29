
from asyncio.windows_events import NULL
from email.quoprimime import body_check
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


my_posts = {2: {"title": "in the grave", "content": "all too well"}}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


def find_post(id):
    try:
        return my_posts[id]
    except:
        return None

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message":"post not found"}
    return {"data": post}

@app.post("/posts")
def create_post(post: Post):
    global my_posts
    post = post.dict()
    id = randrange(0,10000)
    my_posts[id] = post
    print(my_posts)
    return {"message": "added post"}