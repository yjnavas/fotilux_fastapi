from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserInfo(BaseModel):
    id: int
    name: str
    profile_image: Optional[str] = None
    
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentDelete(BaseModel):
    user_id: int

class CommentOut(CommentBase):
    id: int
    created_at: datetime
    post_id: int
    user: Optional[UserInfo] = None
    
    class Config:
        from_attributes = True
