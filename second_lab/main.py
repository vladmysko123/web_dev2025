from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post, user_id)

@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, sort_by: Optional[str] = "id", db: Session = Depends(get_db)):
    return crud.get_posts(db, skip, limit, sort_by)

@app.post("/posts/{post_id}/comments/", response_model=schemas.Comment)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment, post_id)

@app.get("/posts/{post_id}/comments/", response_model=List[schemas.Comment])
def read_comments(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments(db, post_id)
