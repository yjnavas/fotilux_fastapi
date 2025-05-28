from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_db
from app.schemas.token import Token, TokenWithUserData, UserData
from app.utils.auth import authenticate_user, create_access_token

router = APIRouter(
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/token", response_model=TokenWithUserData)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un token JWT mediante login con email y contraseña.
    
    - **username**: Email del usuario (se usa username por compatibilidad con OAuth2)
    - **password**: Contraseña del usuario
    """
    # Autenticar al usuario (username es el email en este caso)
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear el token de acceso con el ID del usuario como subject
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    # Create user data object
    user_data = UserData(
        id=user.id,
        name=user.name,
        mail=user.mail,
        created_at=user.created_at
    )
    
    # Return token with user data
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_data
    }
