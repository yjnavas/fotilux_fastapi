import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """Verify password by hashing the plain password and comparing with stored hash"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user by email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current user from the token (placeholder for JWT implementation)"""
    # This is a simplified version. In a real app, you would decode the JWT token
    # and extract the user_id, then look up the user in the database
    
    # For now, we'll just raise an exception
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token authentication not implemented yet"
    )
