from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    body: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PostWithUserOut(PostOut):
    name: str  # User's name
    file: Optional[str] = None  # File/image path
    
    class Config:
        from_attributes = True
