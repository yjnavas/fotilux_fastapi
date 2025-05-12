from pydantic import BaseModel

class FavoriteOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    
    class Config:
        orm_mode = True
