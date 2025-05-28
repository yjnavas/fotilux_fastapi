from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.comment import Comment
from app.models.user import User
from app.models.media import Media
from fastapi import HTTPException

def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if comment:
        # Buscar la imagen de perfil del usuario (si existe)
        profile_image = db.query(Media).filter(
            and_(
                Media.entity_type == 'user',
                Media.entity_id == comment.user_id
            )
        ).first()
        
        # Si el usuario tiene imagen de perfil, la agregamos al objeto user
        if profile_image:
            comment.user.profile_image = profile_image.url
        else:
            comment.user.profile_image = None
    
    return comment

def get_post_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    # Consulta para obtener comentarios con información del usuario
    comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
    
    # Para cada comentario, buscamos la imagen de perfil del usuario
    for comment in comments:
        # Buscar la imagen de perfil del usuario (si existe)
        profile_image = db.query(Media).filter(
            and_(
                Media.entity_type == 'user',
                Media.entity_id == comment.user_id
            )
        ).first()
        
        # Si el usuario tiene imagen de perfil, la agregamos al objeto user
        if profile_image:
            comment.user.profile_image = profile_image.url
        else:
            comment.user.profile_image = None
    
    return comments

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
