from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from typing import List, Optional
from pydantic import BaseModel

# --- Database setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# --- Models ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")

# --- Schemas ---
class CommentCreate(BaseModel):
    content: str

class CommentOut(CommentCreate):
    id: int
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(PostCreate):
    id: int
    comments: List[CommentOut] = []
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(UserCreate):
    id: int
    posts: List[PostOut] = []
    class Config:
        orm_mode = True

# --- FastAPI app ---
app = FastAPI()

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Create tables ---
Base.metadata.create_all(bind=engine)

# --- Endpoints ---
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.post("/users/{user_id}/posts/", response_model=PostOut)
def create_post(user_id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostOut])
def get_posts(skip: int = 0, limit: int = 10, sort_by: Optional[str] = "id", db: Session = Depends(get_db)):
    sort_column = getattr(Post, sort_by, Post.id)
    return db.query(Post).order_by(sort_column).offset(skip).limit(limit).all()

@app.post("/posts/{post_id}/comments/", response_model=CommentOut)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(content=comment.content, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/posts/{post_id}/comments/", response_model=List[CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
