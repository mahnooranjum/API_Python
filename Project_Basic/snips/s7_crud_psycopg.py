
from asyncio.windows_events import NULL
from email.quoprimime import body_check
from random import randrange
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI()


my_posts = {2: {"title": "in the grave", "content": "all too well"}}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try: 
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password='SQL1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('[INFO] : Database connection successful')
        break 
    except Exception as e: 
        print('[INFO] : Error connecting to the database')
        print('[ERROR] : ', e)
        time.sleep(2)

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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    # print("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,\
                     (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"created": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def del_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    conn.commit()
    return {"deleted": post}



@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, post : Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    post = cursor.fetchone()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    conn.commit()
    return {"updated": post}
