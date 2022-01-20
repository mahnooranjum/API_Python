
from asyncio.windows_events import NULL
from email.quoprimime import body_check
from random import randrange
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
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
def get_post(id: int):

    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    global my_posts
    post = post.dict()
    id = randrange(0,10000)
    my_posts[id] = post
    print(my_posts)
    return {"message": "added post"}


@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def del_post(id: int):

    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    del my_posts[id]
    return {"deleted": post}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, post : Post):

    is_post = find_post(id)
    if not is_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    post = post.dict()
    my_posts[id] = post
    return {"updated": post}
