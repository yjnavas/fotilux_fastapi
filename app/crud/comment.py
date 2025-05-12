from sqlalchemy.orm import Session
from app.models.comment import Comment
from fastapi import HTTPException

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_post_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def create_comment(db: Session, content: str, post_id: int, user_id: int):
    db_comment = Comment(content=content, post_id=post_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, content: str, user_id: int):
    db_comment = get_comment(db, comment_id)
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    db_comment.content = content
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    db_comment = get_comment(db, comment_id)
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(db_comment)
    db.commit()
    return {"status": "success"}
