from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.comment import CommentOut
from app.crud import comment as comment_crud

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{post_id}", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, content: str, user_id: int, db: Session = Depends(get_db)):
    return comment_crud.create_comment(db=db, content=content, post_id=post_id, user_id=user_id)

@router.get("/post/{post_id}", response_model=List[CommentOut])
def read_post_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = comment_crud.get_post_comments(db, post_id=post_id, skip=skip, limit=limit)
    return comments

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, content: str, user_id: int, db: Session = Depends(get_db)):
    return comment_crud.update_comment(db=db, comment_id=comment_id, content=content, user_id=user_id)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return comment_crud.delete_comment(db=db, comment_id=comment_id, user_id=user_id)
