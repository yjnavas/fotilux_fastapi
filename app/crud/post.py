from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from fastapi import HTTPException

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.status == "active").offset(skip).limit(limit).all()

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.user_id == user_id, Post.status == "active").offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_data: PostCreate, user_id: int):
    db_post = get_post(db, post_id)
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    # Update post fields
    for key, value in post_data.dict().items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int, user_id: int):
    db_post = get_post(db, post_id)
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    # Soft delete by changing status
    db_post.status = "deleted"
    db.commit()
    return {"status": "success"}
