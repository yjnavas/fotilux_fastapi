from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserData(BaseModel):
    id: int
    name: str
    mail: EmailStr
    created_at: datetime

class TokenWithUserData(Token):
    user: UserData

class TokenData(BaseModel):
    user_id: Optional[int] = None
