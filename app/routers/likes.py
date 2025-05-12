from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.like import LikeOut
from app.crud import like as like_crud

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{post_id}", response_model=LikeOut, status_code=status.HTTP_201_CREATED)
def create_like(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return like_crud.create_like(db=db, post_id=post_id, user_id=user_id)

@router.get("/post/{post_id}", response_model=List[LikeOut])
def read_post_likes(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    likes = like_crud.get_post_likes(db, post_id=post_id, skip=skip, limit=limit)
    return likes

@router.get("/user/{user_id}", response_model=List[LikeOut])
def read_user_likes(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    likes = like_crud.get_user_likes(db, user_id=user_id, skip=skip, limit=limit)
    return likes

@router.delete("/{post_id}")
def delete_like(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return like_crud.delete_like(db=db, post_id=post_id, user_id=user_id)
