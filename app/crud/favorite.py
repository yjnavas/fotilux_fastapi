from sqlalchemy.orm import Session, joinedload
from app.models.favorite import Favorite
from app.models.post import Post
from app.models.user import User
from fastapi import HTTPException

def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Favorite).filter(Favorite.user_id == user_id).offset(skip).limit(limit).all()

def get_post_favorites(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Favorite).filter(Favorite.post_id == post_id).offset(skip).limit(limit).all()

def create_favorite(db: Session, post_id: int, user_id: int):
    # Check if already favorited
    existing_favorite = db.query(Favorite).filter(
        Favorite.post_id == post_id,
        Favorite.user_id == user_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Post already in favorites")
    
    db_favorite = Favorite(post_id=post_id, user_id=user_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, post_id: int, user_id: int):
    db_favorite = db.query(Favorite).filter(
        Favorite.post_id == post_id,
        Favorite.user_id == user_id
    ).first()
    
    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(db_favorite)
    db.commit()
    return {"status": "success"}

def get_user_favorited_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get posts with user information that the user has favorited for frontend format"""
    return db.query(Post).join(Favorite, Post.id == Favorite.post_id).join(User).filter(
        Favorite.user_id == user_id,
        Post.status == 'active'
    ).options(joinedload(Post.user)).offset(skip).limit(limit).all()
