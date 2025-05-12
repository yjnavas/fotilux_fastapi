from sqlalchemy.orm import Session
from app.models.user import User, Follow
from app.schemas.user import UserCreate
from fastapi import HTTPException
import hashlib

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.mail == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Hash the password
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(name=user.name, mail=user.mail, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def follow_user(db: Session, following_user_id: int, followed_user_id: int):
    # Check if both users exist
    if not get_user(db, following_user_id) or not get_user(db, followed_user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already following
    existing_follow = db.query(Follow).filter(
        Follow.following_user_id == following_user_id,
        Follow.followed_user_id == followed_user_id
    ).first()
    
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")
    
    # Create follow relationship
    db_follow = Follow(following_user_id=following_user_id, followed_user_id=followed_user_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

def unfollow_user(db: Session, following_user_id: int, followed_user_id: int):
    # Check if follow relationship exists
    db_follow = db.query(Follow).filter(
        Follow.following_user_id == following_user_id,
        Follow.followed_user_id == followed_user_id
    ).first()
    
    if not db_follow:
        raise HTTPException(status_code=404, detail="Not following this user")
    
    # Delete follow relationship
    db.delete(db_follow)
    db.commit()
    return {"status": "success"}
