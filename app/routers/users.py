from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.follow import FollowOut
from app.crud import user as user_crud

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.mail)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/follow/{target_id}", response_model=FollowOut)
def follow_user(user_id: int, target_id: int, db: Session = Depends(get_db)):
    return user_crud.follow_user(db, following_user_id=user_id, followed_user_id=target_id)

@router.delete("/{user_id}/unfollow/{target_id}")
def unfollow_user(user_id: int, target_id: int, db: Session = Depends(get_db)):
    return user_crud.unfollow_user(db, following_user_id=user_id, followed_user_id=target_id)
