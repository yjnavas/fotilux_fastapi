from pydantic import BaseModel
from datetime import datetime

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
    
    class Config:
        orm_mode = True
