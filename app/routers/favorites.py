from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.favorite import FavoriteOut
from app.crud import favorite as favorite_crud

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{post_id}", response_model=FavoriteOut, status_code=status.HTTP_201_CREATED)
def create_favorite(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return favorite_crud.create_favorite(db=db, post_id=post_id, user_id=user_id)

@router.get("/user/{user_id}", response_model=List[FavoriteOut])
def read_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = favorite_crud.get_user_favorites(db, user_id=user_id, skip=skip, limit=limit)
    return favorites

@router.delete("/{post_id}")
def delete_favorite(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return favorite_crud.delete_favorite(db=db, post_id=post_id, user_id=user_id)
