from pydantic import BaseModel
from datetime import datetime

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    post_id: int
    user_id: int
    
    class Config:
        from_attributes = True
