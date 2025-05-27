from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.schemas.post import PostCreate, PostOut, PostWithUserOut
from app.crud import post as post_crud
from app.utils.auth import get_current_active_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        print(f"Received post creation request: {post}")
        print(f"Current user: {current_user}")
        result = post_crud.create_post(db=db, post=post, user_id=current_user.id)
        return result
    except Exception as e:
        print(f"Error in create_post endpoint: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")

# @router.get("/", response_model=List[PostOut])
# def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     posts = post_crud.get_posts(db, skip=skip, limit=limit)
#     return posts

@router.get("/", response_model=List[PostWithUserOut])
def read_posts_frontend(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get posts in the format expected by the frontend"""
    db_posts = post_crud.get_posts_with_users(db, skip=skip, limit=limit)
    
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

@router.get("/user/{user_id}", response_model=List[PostOut])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_crud.get_user_posts(db, user_id=user_id, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=PostWithUserOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Verificar si tenemos acceso a los datos del usuario
    if not hasattr(db_post, 'user') or db_post.user is None:
        print("Error: No se pudo acceder a la información del usuario")
        # Intentar cargar el usuario explícitamente
        db.refresh(db_post)
    
    # Crear un diccionario con los datos del post y del usuario
    post_data = {
        "id": db_post.id,
        "body": db_post.body,
        "user_id": db_post.user.id,
        "status": db_post.status,
        "created_at": db_post.created_at,
        "updated_at": db_post.created_at,  # Usando created_at como updated_at si no está disponible
        "name": db_post.user.name if hasattr(db_post, 'user') and db_post.user else None,
        "file": None  # Puedes ajustar esto según tus necesidades
    }
    
    print(f"Post data: {post_data}")
    return post_data

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    return post_crud.delete_post(db=db, post_id=post_id, user_id=current_user.id)
