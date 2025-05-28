from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.schemas.follow import FollowOut
from app.crud import user as user_crud
from app.utils.auth import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    
    Campos requeridos:
    - user_name: Nombre de usuario único
    - mail: Correo electrónico
    - password: Contraseña
    
    Campos opcionales:
    - name: Nombre del usuario
    - last_name: Apellido
    - birth_date: Fecha de nacimiento (formato ISO)
    """
    db_user = user_crud.get_user_by_email(db, email=user.mail)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/follow/{target_id}", response_model=FollowOut)
async def follow_user(user_id: int, target_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Verificar que el usuario autenticado sea el mismo que intenta seguir a otro
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    return user_crud.follow_user(db, following_user_id=user_id, followed_user_id=target_id)

@router.delete("/{user_id}/unfollow/{target_id}")
async def unfollow_user(user_id: int, target_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Verificar que el usuario autenticado sea el mismo que intenta dejar de seguir a otro
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    return user_crud.unfollow_user(db, following_user_id=user_id, followed_user_id=target_id)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    """
    Actualizar información de un usuario
    
    Campos actualizables:
    - name: Nombre del usuario
    - user_name: Nombre de usuario
    - phone: Número de teléfono
    - address: Dirección
    - bio: Biografía
    """
    # Verificar que el usuario autenticado sea el mismo que intenta actualizar su información
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    return user_crud.update_user(db, user_id=user_id, user_update=user_update)
