from pydantic import BaseModel
from datetime import datetime

class FollowOut(BaseModel):
    following_user_id: int
    followed_user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
