from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from datetime import datetime

def get_post(db: Session, post_id: int):
    """Get a single post with user information"""
    return db.query(Post).filter(Post.id == post_id).options(joinedload(Post.user)).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.status == "active").offset(skip).limit(limit).all()

def get_posts_with_users(db: Session, skip: int = 0, limit: int = 100):
    """Get posts with user information for frontend format"""
    return db.query(Post).join(User).filter(Post.status == "active").options(joinedload(Post.user)).offset(skip).limit(limit).all()

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.user_id == user_id, Post.status == "active").offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, user_id: int):
    try:
        print(f"Creating post with data: {post.dict()}, user_id: {user_id}")
        db_post = Post(**post.dict(), user_id=user_id)
        print(f"Post object created: {db_post}")
        db.add(db_post)
        print("Post added to session")
        db.commit()
        print("Session committed")
        db.refresh(db_post)
        print(f"Post created successfully with ID: {db_post.id}")
        return db_post
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        db.rollback()
        raise

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
