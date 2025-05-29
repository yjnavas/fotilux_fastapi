from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.schemas.favorite import FavoriteOut
from app.schemas.post import PostOut, PostWithUserOut
from app.crud import favorite as favorite_crud
from app.utils.auth import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
    responses={404: {"description": "Not found"}},
)

@router.get("/my-posts", response_model=List[PostWithUserOut])
def read_current_user_favorited_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get all posts that the current authenticated user has favorited in the format expected by the frontend"""
    db_posts = favorite_crud.get_user_favorited_posts(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # Transform to frontend format
    result = []
    for post in db_posts:
        # Get file from media relationship if available
        file = None
        if post.media and len(post.media) > 0:
            file = post.media[0].filename
        
        post_dict = {
            "id": post.id,
            "body": post.body,
            "user_id": post.user.id,
            "name": post.user.name,  # Include user name from relationship
            "status": post.status,
            "created_at": post.created_at,
            "updated_at": post.created_at,  # Using created_at as updated_at if not available
            "file": file
        }
        result.append(post_dict)
    
    return result

@router.post("/{post_id}", response_model=FavoriteOut, status_code=status.HTTP_201_CREATED)
def create_favorite(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return favorite_crud.create_favorite(db=db, post_id=post_id, user_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[FavoriteOut])
def read_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = favorite_crud.get_user_favorites(db, user_id=user_id, skip=skip, limit=limit)
    return favorites

@router.get("/post/{post_id}", response_model=List[FavoriteOut])
def read_post_favorites(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = favorite_crud.get_post_favorites(db, post_id=post_id, skip=skip, limit=limit)
    return favorites

@router.delete("/{post_id}")
def delete_favorite(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return favorite_crud.delete_favorite(db=db, post_id=post_id, user_id=current_user.id)
