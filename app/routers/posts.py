from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.post import PostCreate, PostOut
from app.crud import post as post_crud

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    return post_crud.create_post(db=db, post=post, user_id=user_id)

@router.get("/", response_model=List[PostOut])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/user/{user_id}", response_model=List[PostOut])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_crud.get_user_posts(db, user_id=user_id, skip=skip, limit=limit)
    return posts

@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    return post_crud.update_post(db=db, post_id=post_id, post_data=post, user_id=user_id)

@router.delete("/{post_id}")
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return post_crud.delete_post(db=db, post_id=post_id, user_id=user_id)
