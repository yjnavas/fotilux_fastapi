from sqlalchemy.orm import Session
from app.models.favorite import Favorite
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
