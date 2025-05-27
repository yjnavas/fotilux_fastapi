from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.comment import CommentOut
from app.crud import comment as comment_crud
from app.utils.auth import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{post_id}", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, comment_data: dict, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return comment_crud.create_comment(db=db, content=comment_data.get("content"), post_id=post_id, user_id=current_user.id)

@router.get("/post/{post_id}", response_model=List[CommentOut])
def read_post_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = comment_crud.get_post_comments(db, post_id=post_id, skip=skip, limit=limit)
    return comments

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, comment_data: dict, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return comment_crud.update_comment(db=db, comment_id=comment_id, content=comment_data.get("content"), user_id=current_user.id)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return comment_crud.delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
