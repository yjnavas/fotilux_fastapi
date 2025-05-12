from sqlalchemy.orm import Session
from app.models.like import Like
from fastapi import HTTPException

def get_post_likes(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Like).filter(Like.post_id == post_id).offset(skip).limit(limit).all()

def get_user_likes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Like).filter(Like.user_id == user_id).offset(skip).limit(limit).all()

def create_like(db: Session, post_id: int, user_id: int):
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    db_like = Like(post_id=post_id, user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db: Session, post_id: int, user_id: int):
    db_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user_id
    ).first()
    
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(db_like)
    db.commit()
    return {"status": "success"}
