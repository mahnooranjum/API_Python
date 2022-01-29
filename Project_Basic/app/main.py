
from asyncio.windows_events import NULL
from email.quoprimime import body_check
from random import randrange
from statistics import mode
from turtle import title
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models, schemas

from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



my_posts = {2: {"title": "in the grave", "content": "all too well"}}


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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict() )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"created": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def del_post(id: int ,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    post.delete(synchronize_session=False)
    db.commit()
    return {"deleted": post.first()}



@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, post : schemas.PostCreate, db: Session = Depends(get_db)):

    post_db = db.query(models.Post).filter(models.Post.id == id)

    if post_db.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    post_db.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"updated": post_db.first()}
